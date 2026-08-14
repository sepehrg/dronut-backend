from rest_framework.routers import DefaultRouter
from .views import DonutViewSet


router = DefaultRouter()
router.register("donuts", DonutViewSet, basename="donut")

urlpatterns = router.urls