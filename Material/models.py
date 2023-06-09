from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator,MinLengthValidator
from Account.models import User


# Create your models here.
class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    name = models.CharField(unique=True, max_length=256, validators=[MinLengthValidator(1)])

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, validators=[MinLengthValidator(1)])

class Material_Quantity(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    ingredient=models.ForeignKey(Material,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(unique=True,max_length=256, validators=[MinLengthValidator(1)])
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Material_Stock(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    max_capacity = models.PositiveIntegerField()
    current_capacity = models.PositiveIntegerField()

