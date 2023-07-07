from Store.services.store_services import get_store_service,get_product_service,create_product_service
from Material.models import MaterialStock,Material,MaterialQuantity

"""
Material Stock Service
"""

# list all material stock associate with a store 
def list_material_stock_service(request, store_uuid):
    store = get_store_service(request.user, store_uuid)
    if not store:
        return False
    inventory = MaterialStock.objects.filter(store = store)
    if not inventory:
        return False
    return inventory

# To check if the max_capacity is lower than current capacity, if yes return current capacity else, return max capacity
def check_and_return_valid_max_capacity(max_capacity, current_capacity):
    if max_capacity < current_capacity:
        return current_capacity
    return max_capacity

# check if the user already has a material stock with that material, if yes return False, otherwise return True
def check_material_stock_available(store,material):
    try:
        material_stock = MaterialStock.objects.get(material = material, store=store)
        if material_stock:
            return False
    except:
        return True

# create material stock
def create_material_stock_service(request, store_uuid, material_uuid):
    try:
        material = Material.objects.get(material_uuid = material_uuid)
        store = get_store_service(request.user, store_uuid)
        if material and store and check_material_stock_available(store,material):
            material_stock = MaterialStock.objects.create(material = material, store=store,
                                                        current_capacity  = int(request.data["current_capacity"]),
                                                        max_capacity = check_and_return_valid_max_capacity(int(request.data["max_capacity"]),
                                                                                                            int(request.data["current_capacity"])))
            if material_stock:
                return material_stock
        return False
    except:
        return False
    
"""
Material Quantity Service
"""

# create material quantity for a product that is associate with a store 
def create_material_quantity_service(request, store_uuid, material_uuid, product_uuid, quantity=None):
    quantity = quantity
    try:
        quantity = request.data["quantity"]
    except:
        pass
    try:
        material = Material.objects.get(material_uuid = material_uuid)
        product = get_product_service(request, store_uuid = store_uuid, product_uuid = product_uuid)
        material_quantity = MaterialQuantity.objects.create(ingredient = material, product = product, quantity = quantity)
        if material_quantity:
            return material_quantity
        return False
    except:
        return False

# list all material quantity for a product that is associate with a store 
def list_material_quantity_service(request, store_uuid, product_uuid):
    try:
        product = get_product_service(request, store_uuid=store_uuid, product_uuid = product_uuid)
        material_quantity = MaterialQuantity.objects.filter(product = product)
        if material_quantity:
            return material_quantity
        return False
    except:
        return False
    
"""
Material Restock Service
"""

# return the quantity of material and total price to restock a type of material
def check_for_restock(material_stock_uuid):
    try:
        material_stock = MaterialStock.objects.get(material_stock_uuid = material_stock_uuid)
        # minus the current capacity of material stock using max capacity to get the amount require to restock
        amount_to_restock = material_stock.max_capacity - material_stock.current_capacity
        material = Material.objects.get(material_uuid = material_stock.material.material_uuid)
        # times the amount_to_restock with material price to get total price
        price = amount_to_restock * material.price
        return price
    except:
        return None
    
# return retocked material stock or false after a request for restock was made
def request_for_restock(material_stock_uuid):
    try:
        material_stock = MaterialStock.objects.get(material_stock_uuid = material_stock_uuid)
        amount_restocked = material_stock.max_capacity - material_stock.current_capacity
        material_stock.current_capacity = material_stock.max_capacity
        material_stock.save()
        return amount_restocked
    except:
        return False
  
# return a list of material that haven't been used for material stock creation for a store as duplicate material stock is not allowed
def return_all_available_material_for_stock_creation(request, store_uuid):
    material = Material.objects.all()
    material_stock = list_material_stock_service(request, store_uuid)
    if not material_stock:
        return material
    material_stock_material_uuid = [m_s.material.material_uuid for m_s in material_stock]
    available_material = material.exclude(material_uuid__in = material_stock_material_uuid) 
    return available_material

# return a list of material that haven't been used for certain product as duplicate material quantity is not allowed
def return_all_available_material_for_material_quantity_creation(request, store_uuid, product_uuid):
    material_quantity = list_material_quantity_service(request, store_uuid, product_uuid)
    if not material_quantity:
        return False
    material_uuid_array = [m_q.ingredient.material_uuid for m_q in material_quantity]
    material_quantity_array = Material.objects.all()
    available_material = material_quantity_array.exclude(material_uuid__in = material_uuid_array) 
    return available_material

# create product then loop through the request_material_quantity_array (array structure: [<uuid>,<quantity>...])
# to create material quantity and add the product to the product foreign key field
def create_product_and_material_quantity_service(request, store_uuid, request_material_quantity_array):
    index = 1
    try:
        product = create_product_service(request,store_uuid)
        if product:
            for element in request_material_quantity_array:
                # element here is the key for the value of material_uuid
                # request_material_quantity_array[index] is the key for the value of material quantity
                material_uuid = request.data[element]
                quantity = request.data[request_material_quantity_array[index]]
                create_material_quantity_service(request, store_uuid, material_uuid, product.product_uuid, quantity)
                request_material_quantity_array.pop(index)
                index += 1
            return True
        return False
    except:
        False