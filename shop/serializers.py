from rest_framework import serializers
from .models import Donut, Order, OrderItem

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


class OrderSelectionSerializer(serializers.Serializer):
  donut_code = serializers.CharField(max_length=100)
  quantity = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
  donuts = OrderSelectionSerializer(many=True, min_length=1)


class OrderItemSerializer(serializers.ModelSerializer):
  donut_code = serializers.CharField(source="donut.code", read_only=True)

  class Meta:
    model = OrderItem
    fields = ["donut_code", "quantity", "unit_price"]


class OrderSerializer(serializers.ModelSerializer):
  items = OrderItemSerializer(many=True, read_only=True)

  class Meta:
    model = Order
    fields = ["id", "status", "total", "items"]
