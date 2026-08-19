from django.contrib import admin

from .models import Donut, Order, OrderItem


@admin.register(Donut)
class DonutAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "price", "is_available")
    list_filter = ("is_available",)
    search_fields = ("code", "name", "description")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    fields = ("donut", "quantity", "unit_price")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "total", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("=id", "items__donut__code")
    readonly_fields = ("id", "status", "total", "created_at")
    inlines = (OrderItemInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("items__donut")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
