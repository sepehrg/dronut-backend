from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.db.models import Q

from .models import Donut, Order
from .serializers import CreateOrderSerializer, DonutSerializer, OrderSerializer
from .services.orders import create_order, dispatch_order

class DonutViewSet(ModelViewSet):
  queryset = Donut.objects.all()
  serializer_class = DonutSerializer

  def get_queryset(self):
    queryset = super().get_queryset()

    query = self.request.query_params.get("query")

    if query:
      queryset = queryset.filter(Q(name__icontains = query) | Q(description__icontains = query))

    return queryset


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
  queryset = Order.objects.prefetch_related("items__donut")

  def get_serializer_class(self):
    if self.action == "create":
      return CreateOrderSerializer
    return OrderSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order = create_order(serializer.validated_data["donuts"])
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

  @action(detail=True, methods=["post"], url_path="dispatch", url_name="dispatch")
  def mark_dispatched(self, request, pk=None):
    order = dispatch_order(self.get_object())
    return Response(OrderSerializer(order).data)

    
