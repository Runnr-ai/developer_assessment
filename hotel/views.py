from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from hotel import pms_systems

from hotel.models import Hotel, Guest


def chat(request):

    context = {
        "hotel": Hotel.objects.first(),
        "guest": Guest.objects.first(),
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
            "guest": {
                "name": Guest.objects.first().name,
                "phone": Guest.objects.first().phone,
            },
            "all_guests": [
                {"name": guest.name, "phone": guest.phone} for guest in Guest.objects.all()
            ],
        },
    )

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
