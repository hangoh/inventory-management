from Material.models import Store,Product

"""
Store Services
"""

# return a list of store associate with the user
def get_stores_service(user):
    stores = Store.objects.filter(user=user)
    if not stores:
        return False
    return stores

# return store that got by id
def get_store_service(user,id):
    stores = Store.objects.filter(user=user)
    if not stores:
        return False
    try:
        store = stores.get(store_id=id)
        return store
    except:
        return False

# check if store name provided is unique
def store_name_unique(request):
    try:
        store = Store.objects.get(store_name=request.data["store_name"])
        if store:
            return False
    except:
        return True

# create a store with provided store_name
def create_store(request):
    store_name_valid = store_name_unique(request)
    if store_name_valid:
        store = Store.objects.create(store_name = request.data["store_name"], user=request.user)
        store.save()
        return store
    return False

# update store name of a specific id
def update_store_name_service(request,store_id):
    store = get_store_service(request.user,store_id)
    if store:
        store.store_name = request.data["store_name"]
        store.save()
        return store
    return False

# delete store of a specific id
def delete_store_service(request,store_id):
    store = get_store_service(request.user,store_id)
    if store:
        store.delete()
        return True
    return False

"""
Product Services
"""

# list all product in a specific store
def list_product_service(request,store_id):
    store = get_store_service(request.user,store_id)
    if not store:
        return False
    product = store.products.all()
    if not product:
        return False
    return product

# get a product of a specific id associate with a specific store
def get_product_service(request,store_id,product_id):
    products = list_product_service(request,store_id=store_id)
    if not products:
        return False
    try:
        product = products.get(id = product_id)
        return product
    except:
        return False

# update a product of a specific id associate with a specific store
def update_product_name_service(request,store_id,product_id):
    product = get_product_service(request,store_id,product_id)
    if product:
        product.name = request.data["name"]
        product.save()
        return product
    return False

# delete a product of a specific id associate with a specific store
def delete_product_service(request,store_id,product_id):
    product = get_product_service(request,store_id,product_id)
    if product:
        product.delete()
        return True
    return False

#create product with provided product name and add the product to store with provided store_id
def create_product(request,store_id):
    store = get_store_service(request.user,store_id)
    if not store:
        return False
    product = Product.objects.create(name=request.data["name"])
    product.save()
    store.products.add(product)
    return product
