from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Donut


class DonutTests(APITestCase):

    def test_list_donuts(self):
        Donut.objects.create(
            code="CHOCOLATE-01",
            name="Chocolate donut",
            description="Chocolate donut description",
            price=Decimal("3.50"),
            is_available=True,
        )

        response = self.client.get(reverse("donut-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["code"], "CHOCOLATE-01")


    def test_get_donut(self):
        donut = Donut.objects.create(
            code="CHOCOLATE-01",
            name="Chocolate donut",
            description="Chocolate donut description",
            price=Decimal("3.50"),
            is_available=True,
        )

        response = self.client.get(reverse("donut-detail", args=[donut.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
              {
                  "id": donut.id,
                  "name": "Chocolate donut",
                  "code": "CHOCOLATE-01",
                  "description":"Chocolate donut description",
                  "price": "3.50",
                  "is_available": True,
              }
          )

