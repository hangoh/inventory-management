from decimal import Decimal
from uuid import uuid4

from django.db import models
from django.db.models import Q,F

from Store.models import Product, Store

# Create your models here.

class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    name = models.CharField(unique=True, max_length=256)
    material_uuid = models.UUIDField(db_index=True,default=uuid4,editable=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check = ~models.Q(name=""),
                name = "material_name_not_empty"
            ),
            models.CheckConstraint(
                check = Q(price__gte = 0.01),
                name = "material_price_gte_0.01"
            )
        ]


class MaterialQuantity(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    ingredient=models.ForeignKey(Material,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    material_quantity_uuid = models.UUIDField(db_index=True,default=uuid4,editable=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check = Q(quantity__gte = 1),
                name = "quantity_greater_gte_1" 
            )
        ]


class MaterialStock(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    max_capacity = models.PositiveIntegerField()
    current_capacity = models.PositiveIntegerField()
    material_stock_uuid = models.UUIDField(db_index=True,default=uuid4,editable=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check = Q(current_capacity__lte = F("max_capacity")),
                name = "current_capacity_lte_max_capacity" 
            )
        ]



