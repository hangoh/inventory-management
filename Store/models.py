from uuid import uuid4

from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, validators=[MinLengthValidator(1)])
    product_uuid = models.UUIDField(db_index=True,default=uuid4,editable=False)

    def __str__(self):
        return self.name


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(unique=True,max_length=256, validators=[MinLengthValidator(1)])
    products = models.ManyToManyField(Product, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_uuid = models.UUIDField(db_index=True,default=uuid4,editable=False)

    def __str__(self):
        return self.store_name
