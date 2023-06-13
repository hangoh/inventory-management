import factory
from factory.django import DjangoModelFactory

from Material.models import Material, Material_Quantity,Material_Stock
from Store.tests.factories import StoreFactory,ProductFactory

class MaterialFactory(DjangoModelFactory):
    class Meta:
        model = Material

    # The Id will always be the total object count of Material + 1, if the Id is not provided
    material_id = factory.LazyAttribute(lambda n:Material.objects.all().count()+1)
    price = 2.00
    name = ""

class MaterialQuantityFactory(DjangoModelFactory):
    class Meta:
        model = Material_Quantity

    # The Id will always be the total object count of Material Quantity + 1, if the Id is not provided
    id = factory.LazyAttribute(lambda n:Material_Quantity.objects.all().count()+1)
    quantity = 10
    product = factory.SubFactory(ProductFactory)
    ingredient = factory.SubFactory(MaterialFactory)

class MaterialStockFactory(DjangoModelFactory):
    class Meta:
        model = Material_Stock

    # The Id will always be the total object count of Material Stock + 1, if the Id is not provided
    id = factory.LazyAttribute(lambda n:Material_Stock.objects.all().count()+1)
    material = factory.SubFactory(MaterialFactory)
    store = factory.SubFactory(StoreFactory)
    max_capacity = 100
    current_capacity = 50
