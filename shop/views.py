from rest_framework.viewsets import ModelViewSet

from .models import Donut
from .serializers import DonutSerializer

class DonutViewSet(ModelViewSet):
  queryset = Donut.objects.all()
  serializer_class = DonutSerializer

