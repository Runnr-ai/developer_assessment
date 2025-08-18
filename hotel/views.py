from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

from hotel import pms_systems

from hotel.models import Hotel, Guest


def chat(request):

    context = {
        "hotel": Hotel.objects.first(),
        "all_guests": Guest.objects.all(),
    }

    return render(
        request,
        "hotel/chat.html",
        context,
    )

def chat_data(request):
    return JsonResponse(
        {
            "hotel_name": Hotel.objects.first().name,
            "all_guests": [
                {"name": guest.name} for guest in Guest.objects.all()
            ],
        },
    )

def guest_data(request, guest_id):
    try:
        guest = Guest.objects.get(id=guest_id)
    except Guest.DoesNotExist:
        raise Http404("Guest not found")

    data = {
        "name": guest.name,
        "phone": guest.phone,
        "language": guest.language,
        "stays": [
            {
                "hotel": stay.hotel.name,
                "checkin": stay.checkin.isoformat() if stay.checkin else None,
                "checkout": stay.checkout.isoformat() if stay.checkout else None,
            }
            for stay in guest.stays.all()
        ],
    }

    return JsonResponse(data)

@csrf_exempt
@require_POST
def webhook(request, pms_name):
    """
    Assume a webhook call from the PMS with a status update for a reservation.
    The webhook call is a POST request to the url: /webhook/<pms_name>/
    The body of the request should always be a valid JSON string and contain the needed information to perform an update.
    """

    pms_cls = pms_systems.get_pms(pms_name)

    cleaned_webhook_payload = pms_cls.clean_webhook_payload(request.body)
    if not cleaned_webhook_payload:
        return HttpResponse(status=400)
    hotel = Hotel.objects.get(id=cleaned_webhook_payload["hotel_id"])
    pms = hotel.get_pms()
    success = pms.handle_webhook(cleaned_webhook_payload["data"])

    if not success:
        return HttpResponse(status=400)
    else:
        return HttpResponse("Thanks for the update.")
