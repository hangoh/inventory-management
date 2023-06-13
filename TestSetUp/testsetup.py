from django.contrib.auth.models import User
from Material.models import Store,Product,Material,Material_Stock

def initialAccountStoreSetUp(self):
    #create first user and 2 store associate with the user
    p="JustPassword"

    self.user = User.objects.create_user(username="UncleBen", password=p)
    Store.objects.create(store_name = "UncleBen'S" ,user = self.user)
    Store.objects.create(store_name = "UncleBen'S_2", user = self.user)

    #create second user and 1 store associate with the user
    self.user2 = User.objects.create_user(username="UncleBob", password=p)
    Store.objects.create(store_name = "UncleBob'S" ,user = self.user2)

    #create third user and 0 store associate with the user
    self.user3 = User.objects.create_user(username="UncleBam", password=p)

def initialProductSetUp(self):
    # add two new product to store of store id 1 that associate with user of id 1
    product_1 = Product.objects.create(name="Chair")
    product_2 = Product.objects.create(name="table")
    store_1 = Store.objects.get(store_id = 1)
    store_1.products.add(product_1)
    store_1.products.add(product_2)


    # add one new product to store of store id 3 that associate with user of id 2
    store_3 = Store.objects.get(store_id = 3)
    store_3.products.add(product_1)

    # create three material 
    material_1=Material.objects.create(price=5.00,name="wood",store=store_1)
    material_2=Material.objects.create(price=1.30,name="plastic",store=store_3)
    material_3=Material.objects.create(price=10.50,name="steel",store=store_3)

    # material stock for store_id 1  for user id 1
    Material_Stock.objects.create(max_capacity=200,current_capacity=104,material=material_1,store=store_1)
    Material_Stock.objects.create(max_capacity=100,current_capacity=45,material=material_3,store=store_1)

    #material stock for store_id 3 for user id 2
    Material_Stock.objects.create(max_capacity=230,current_capacity=144,material=material_2,store=store_3)