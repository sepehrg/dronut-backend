from rest_framework.routers import DefaultRouter
from .views import DonutViewSet, OrderViewSet


router = DefaultRouter()
router.register("donuts", DonutViewSet, basename="donut")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = router.urls
