from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Donut


class DonutListTests(APITestCase):

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