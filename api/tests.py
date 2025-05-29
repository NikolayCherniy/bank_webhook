import uuid

from rest_framework.test import APITestCase

from api.models import BalanceLog, Organization
from api.services import apply_incoming_payment


class WebhookTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/webhook/bank/"
        self.payload = {
            "operation_id": str(uuid.uuid4()),
            "amount": 1000,
            "payer_inn": "1234567890",
            "document_number": "PAY-1",
            "document_date": "2024-04-27T21:00:00Z",
        }

    def test_new_payment_creates_record_and_updates_balance(self):
        response = self.client.post(self.url, data=self.payload)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            BalanceLog.objects.filter(
                operation_id=self.payload["operation_id"]
            ).exists()
        )

        organization = Organization.objects.get(inn=self.payload["payer_inn"])
        self.assertEqual(organization.balance, self.payload["amount"])

    def test_duplicate_payment_does_not_update_balance(self):
        self.client.post(self.url, data=self.payload)
        response = self.client.post(
            self.url, data=self.payload, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            BalanceLog.objects.filter(
                operation_id=self.payload["operation_id"]
            ).count(),
            1,
        )

        organization = Organization.objects.get(inn=self.payload["payer_inn"])
        self.assertEqual(organization.balance, self.payload["amount"])


class BalanceViewTestCase(APITestCase):
    def setUp(self):
        self.inn = "9999999999"

        for amount in (5000, 3000):
            apply_incoming_payment(
                {
                    "payer_inn": self.inn,
                    "amount": amount,
                    "operation_id": uuid.uuid4(),
                    "document_number": "PAY-X",
                    "document_date": "2024-04-27T21:00:00Z",
                },
            )

    def test_balance_endpoint_returns_correct_balance(self):
        response = self.client.get(f"/api/organizations/{self.inn}/balance/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"inn": self.inn, "balance": 8000})
