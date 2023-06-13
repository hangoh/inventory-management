import factory
from factory.django import DjangoModelFactory

from Account.tests.tests_model import UserModelFactory
from Material.models import Store
from Material.models import Product

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
    
    # The Id will always be the total object count of Product + 1, if the Id is not provided
    id = factory.LazyAttribute(lambda n:Product.objects.all().count()+1)
    name = ""


class StoreFactory(DjangoModelFactory):
    class Meta:
        model = Store
    
    # The Id will always be the total object count of Product + 1, if the Id is not provided
    store_id = factory.LazyAttribute(lambda n:Store.objects.all().count()+1)
    store_name = ""
    user = factory.SubFactory(UserModelFactory)


    #Required for many to many relationship field
    @factory.post_generation
    def products(self,create,extrated,**kwargs):
        if not create:
            return
        if extrated:
            for product in extrated:
                self.products.add(product)
