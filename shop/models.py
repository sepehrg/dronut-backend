from django.db import models

class Donut(models.Model):
  name = models.CharField(max_length=200)
  code = models.CharField(max_length=100, unique=True)
  description = models.TextField()
  price = models.DecimalField(max_digits=6, decimal_places=2)
  is_available = models.BooleanField(default=True)

