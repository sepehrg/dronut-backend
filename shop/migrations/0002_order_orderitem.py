# Generated manually for the order domain.

import uuid

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("status", models.CharField(choices=[("CREATED", "Created"), ("DISPATCHED", "Dispatched")], default="CREATED", max_length=20)),
                ("total", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField()),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=6)),
                ("donut", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="shop.donut")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="shop.order")),
            ],
        ),
    ]
