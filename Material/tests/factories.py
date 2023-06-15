import factory
from factory.django import DjangoModelFactory

from Material.models import Material, MaterialQuantity,MaterialStock
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
        model = MaterialQuantity

    # The Id will always be the total object count of Material Quantity + 1, if the Id is not provided
    id = factory.LazyAttribute(lambda n:MaterialQuantity.objects.all().count()+1)
    quantity = 10
    product = factory.SubFactory(ProductFactory)
    ingredient = factory.SubFactory(MaterialFactory)

class MaterialStockFactory(DjangoModelFactory):
    class Meta:
        model = MaterialStock

    # The Id will always be the total object count of Material Stock + 1, if the Id is not provided
    id = factory.LazyAttribute(lambda n:MaterialStock.objects.all().count()+1)
    material = factory.SubFactory(MaterialFactory)
    store = factory.SubFactory(StoreFactory)
    max_capacity = 100
    current_capacity = 50
