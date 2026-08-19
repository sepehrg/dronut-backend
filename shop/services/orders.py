from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from shop.models import Donut, Order, OrderItem


@transaction.atomic
def create_order(selections):
    """Create an order from validated request or message data."""
    codes = [selection["donut_code"] for selection in selections]
    donuts_by_code = {
        donut.code: donut
        for donut in Donut.objects.select_for_update().filter(code__in=codes)
    }

    unknown_codes = sorted(set(codes) - donuts_by_code.keys())
    if unknown_codes:
        raise ValidationError({"donuts": [f"Unknown donut code: {code}" for code in unknown_codes]})

    unavailable_codes = sorted(
        code for code in codes if not donuts_by_code[code].is_available
    )
    if unavailable_codes:
        raise ValidationError(
            {"donuts": [f"Donut is unavailable: {code}" for code in unavailable_codes]}
        )

    total = sum(
        (donuts_by_code[selection["donut_code"]].price * selection["quantity"]
         for selection in selections),
        Decimal("0.00"),
    )
    order = Order.objects.create(total=total)
    OrderItem.objects.bulk_create(
        [
            OrderItem(
                order=order,
                donut=donuts_by_code[selection["donut_code"]],
                quantity=selection["quantity"],
                unit_price=donuts_by_code[selection["donut_code"]].price,
            )
            for selection in selections
        ]
    )
    return order


@transaction.atomic
def dispatch_order(order):
    if order.status != Order.Status.CREATED:
        raise ValidationError({"status": "Only created orders can be dispatched."})

    order.status = Order.Status.DISPATCHED
    order.save(update_fields=["status"])
    return order
