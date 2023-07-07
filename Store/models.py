from uuid import uuid4

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    product_uuid = models.UUIDField(db_index=True,default=uuid4,editable=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check = ~models.Q(name=""),
                name = "name_not_empty"
            )
        ]


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(unique=True,max_length=256)
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_uuid = models.UUIDField(db_index=True,default=uuid4,editable=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check = ~models.Q(store_name=""),
                name = "store_name_not_empty"
            )
        ]

