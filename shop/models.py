import uuid

from django.db import models


class Donut(models.Model):
  name = models.CharField(max_length=200)
  code = models.CharField(max_length=100, unique=True)
  description = models.TextField()
  price = models.DecimalField(max_digits=6, decimal_places=2)
  is_available = models.BooleanField(default=True)


class Order(models.Model):
  class Status(models.TextChoices):
    CREATED = "CREATED", "Created"
    DISPATCHED = "DISPATCHED", "Dispatched"

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
  total = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
  donut = models.ForeignKey(Donut, on_delete=models.PROTECT)
  quantity = models.PositiveIntegerField()
  unit_price = models.DecimalField(max_digits=6, decimal_places=2)
