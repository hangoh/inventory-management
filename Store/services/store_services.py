import json

from Store.models import Store,Product
from Material.models import MaterialQuantity, MaterialStock
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
def get_store_service(user,uuid):
    stores = Store.objects.filter(user=user)
    if not stores:  
        return False
    try:
        store = stores.get(store_uuid=uuid)
        return store
    except:
        return False
    
def create_store_service(request):
    try:
        print(request.data)
        store = Store.objects.create(user = request.user, store_name = request.data['store_name'])
        return store
    except:
        return False

"""
Product Services
"""

# list all product in a specific store
def list_product_service(request,store_uuid):
    store = get_store_service(request.user,store_uuid)
    if not store:
        return False
    products = store.products.all()
    if not products:
        return False
    return products

# get a product of a specific id associate with a specific store
def get_product_service(request,store_uuid,product_uuid):
    products = list_product_service(request,store_uuid=store_uuid)
    if not products:
        return False
    try:
        product = products.get(product_uuid = product_uuid)
        return product
    except:
        return False

# create product with provided product name and add the product to store with provided store_id
def create_product_service(request,store_uuid):
    store = get_store_service(request.user,store_uuid)
    if not store:
        return False
    product = Product.objects.create(name=request.data["name"])
    product.save()
    store.products.add(product)
    return product

# calculate the quantity of each product that can be produce before any material become insufficeint
def calculate_remaining_product_quantity_service(material_quantity, material_stock_current_capacity):
    """
    The logic is that if any of the number in material_stock_current_capacity 
    is less than(<) zero than it will return the current quantity since all material should 
    have the sufficient amount to produce the product
    """
    material_sufficient = True
    quantity = 0
    # only execute the logic below if both material quantity and material stock current capacity array are not empty
    if material_quantity != [] and material_stock_current_capacity != []:
        while material_sufficient:
            # loop through material stock current capacity
            current_index = 0
            for each_stock_capacity in material_stock_current_capacity:
                # if material stock current capacity minus material quantity is negative, return the current quantity else quantity + 1
                if not (each_stock_capacity - material_quantity[current_index] >= 0):
                    material_sufficient = False
                    return quantity
                material_stock_current_capacity[current_index] -= material_quantity[current_index]
                if current_index < len(material_quantity):
                    current_index += 1
            quantity += 1
    return quantity


"""
services or function related to updating the db for product sales 
"""

def check_if_quantity_sold_is_valid(material_quantity_array, store):
    """
    loop through the material_quantity_array and get the associate material stock objects then
    check if the current capacity of material stock is larger than the quantity of sales.
    check all quantity before changing the value since if any of the material stock quantity is lower 
    than the sales quantity, the product sales quantity is error or invalid. 
    """
    for material_quantity in material_quantity_array:
        material_stock = MaterialStock.objects.get(material = material_quantity["material"], store = store)
        if material_stock.current_capacity - material_quantity["quantity"]<0:
            return False
    return True

def save_quantity_sold_changes_to_db(material_quantity_array, store):
    """
    loop through the material_quantity_array and get the associate material stock objects then
    abstract the quantity from material stock current capacity then save the db changes
    """
    for material_quantity in material_quantity_array:
        material_stock = MaterialStock.objects.get(material = material_quantity["material"], store = store)
        material_stock.current_capacity = material_stock.current_capacity - material_quantity["quantity"]
        material_stock.save()
            
# get the quantity of item sold from a post request and than abstract all material quantity of the product from material stock
def calculate_item_sold(request, quantity, store_uuid, product_uuid):
    """
    get all material quantity that is equal to the material quantity required for 
    all the sold product into an array, than abstract the material stock current capacity 
    according to material and quantity in the array 
    """
    try:
        material_quantity_array=[]
        # get all material required by the product
        product = get_product_service(request, store_uuid, product_uuid)
        materials = MaterialQuantity.objects.filter(product = product)
        store = Store.objects.get(store_uuid = store_uuid)
        if not materials:
            return False
        # loop through the materials and append material and quantity set 
        # {"material" : material,"quantity" : material.quantity*quantity} into the array
        for material in materials:
            material_quantity_array.append({"material" : material.ingredient, "quantity" : int(material.quantity*quantity)})
        if not check_if_quantity_sold_is_valid(material_quantity_array, store):
            return False
        save_quantity_sold_changes_to_db(material_quantity_array, store)
        return {"product" : product_uuid, "quantity" : quantity}
    except:
        return False
    
# service to handle request to update material stock according to sale
def product_sales_services(request, store_uuid):
    products = request.data['products']
    if type(products) == str:
        products = json.loads(products)
    response = {"sale":[],"error":[]}
    # loop through all the product from POST request to update each material stock accordingly
    for product in products:
        result = calculate_item_sold(request, product["quantity"], store_uuid, product["uuid"])
        if not result:
            # return error message and uuid product if faile to update the material stock
            response["error"].append({"product": product["uuid"],"error":"Fail to Update Sale For This Product uuid {}".format(product["uuid"])})
        else:
            response["sale"].append(result)
    return response

# check if there are duplicate identical material_uuid in the array as a product is not allowed to have more than 1 material quantity of the same material
def check_material_quantity_duplicate(request, request_material_quantity_array):
    # the array structure will be dict key array ( exp : ["material_uuid_1", ""material_uuid_1_qunatity"...]) to get value from request.data, index of odd will be the uuid 
    # return true if there are duplicate identical material
    uuid_array=[]
    index = 0
    #loop through the array to extract uuid, than remove the next element from the array which is the quantity
    for i in range(int(len(request_material_quantity_array)/2)):
        uuid_array.append(request.data[request_material_quantity_array[index]])
        index += 2
    for uuid in uuid_array:
        if uuid_array.count(uuid) != 1:
            return True
    return False

