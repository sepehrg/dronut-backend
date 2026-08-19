from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Donut


class OrderCreationTests(APITestCase):
    def setUp(self):
        self.homer = Donut.objects.create(
            code="THE_HOMER",
            name="The Homer",
            description="Pink iced donut with sprinkles",
            price=Decimal("3.50"),
            is_available=True,
        )
        self.unavailable = Donut.objects.create(
            code="SOLD_OUT",
            name="Sold out donut",
            description="Not currently orderable",
            price=Decimal("4.00"),
            is_available=False,
        )

    def test_creates_order_and_calculates_total_on_server(self):
        response = self.client.post(
            reverse("order-list"),
            {
                "donuts": [
                    {"donut_code": "THE_HOMER", "quantity": 3},
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "CREATED")
        self.assertEqual(response.data["total"], "10.50")
        self.assertEqual(response.data["items"], [
            {
                "donut_code": "THE_HOMER",
                "quantity": 3,
                "unit_price": "3.50",
            }
        ])

    def test_rejects_zero_or_negative_quantities(self):
        for quantity in (0, -1):
            with self.subTest(quantity=quantity):
                response = self.client.post(
                    reverse("order-list"),
                    {"donuts": [{"donut_code": "THE_HOMER", "quantity": quantity}]},
                    format="json",
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rejects_unavailable_donut(self):
        response = self.client.post(
            reverse("order-list"),
            {"donuts": [{"donut_code": "SOLD_OUT", "quantity": 1}]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("SOLD_OUT", str(response.data))

    def test_rejects_unknown_donut(self):
        response = self.client.post(
            reverse("order-list"),
            {"donuts": [{"donut_code": "UNKNOWN", "quantity": 1}]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("UNKNOWN", str(response.data))

    def test_dispatches_a_created_order(self):
        created = self.client.post(
            reverse("order-list"),
            {"donuts": [{"donut_code": "THE_HOMER", "quantity": 1}]},
            format="json",
        )

        response = self.client.post(reverse("order-dispatch", args=[created.data["id"]]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "DISPATCHED")
