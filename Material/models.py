from uuid import uuid4

from django.db import models
from django.core.validators import MinLengthValidator

from Store.models import Product, Store


# Create your models here.
class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    name = models.CharField(unique=True, max_length=256, validators=[MinLengthValidator(1)])
    uuid = models.UUIDField(db_index=True,default=uuid4,editable=False)


class MaterialQuantity(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    ingredient=models.ForeignKey(Material,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    uuid = models.UUIDField(db_index=True,default=uuid4,editable=False)


class MaterialStock(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    max_capacity = models.PositiveIntegerField()
    current_capacity = models.PositiveIntegerField()
    uuid = models.UUIDField(db_index=True,default=uuid4,editable=False)



