import django.test

from hotel.models import Stay, Hotel, Guest

from hotel.tests import load_api_fixture
from hotel.tests.factories import HotelFactory


class PMS_Apaleotest(django.test.TestCase):
    def setUp(self) -> None:
        self.hotel = HotelFactory(pms=Hotel.PMS.APALEO)
        self.pms = self.hotel.get_pms()

    def test_clean_webhook_payload_faulty(self):
        cleaned_payload = self.pms.clean_webhook_payload(load_api_fixture("webhook_payload_faulty.json"))
        self.assertIsNone(cleaned_payload)

    def test_clean_webhook_payload(self):
        cleaned_payload = self.pms.clean_webhook_payload(load_api_fixture("webhook_payload.json"))
        if not cleaned_payload:
            self.fail("No cleaned payload returned")
        else:
            self.assertIsInstance(cleaned_payload, dict)
            self.assertEqual(cleaned_payload["hotel_id"], self.hotel.id)
            self.assertIsInstance(cleaned_payload["data"], dict)

    def test_handle_webhook(self):
        cleaned_payload = self.pms.clean_webhook_payload(load_api_fixture("webhook_payload.json"))
        success = self.pms.handle_webhook(cleaned_payload)
        self.assertTrue(success)
        stays = Stay.objects.filter(hotel=self.hotel)
        self.assertEqual(stays.count(), 3)
        guests = Guest.objects.all()
        self.assertEqual(guests.count(), 3)
