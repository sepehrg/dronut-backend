from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from .models import Donut
from .serializers import DonutSerializer

class DonutViewSet(ModelViewSet):
  queryset = Donut.objects.all()
  serializer_class = DonutSerializer

  def get_queryset(self):
    queryset = super().get_queryset()

    query = self.request.query_params.get("query")

    if query:
      queryset = queryset.filter(Q(name__icontains = query) | Q(description__icontains = query))

    return queryset

    
