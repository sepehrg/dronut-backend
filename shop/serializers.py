from rest_framework import serializers
from .models import Donut

class DonutSerializer(serializers.ModelSerializer):
  class Meta: 
    model = Donut
    fields = [
      "id",
      "name",
      "code",
      "description",
      "price",
      "is_available",
    ]
