from Store.services.store_services import get_store_service,get_product_service
from Material.models import MaterialStock,Material,MaterialQuantity

"""
Material Service
"""

# return all material
def list_material_service():
    material = Material.objects.all()
    if not material:
        return False
    return material   

# create material 
def create_material_service(request):
    material = Material.objects.create(name = request.data["name"], price=request.data["price"])
    if material:
        return material
    return False

# update material
def update_material_service(request,material_uuid):
    try:
        material = Material.objects.get(uuid=material_uuid)
        material.price = request.data["price"]
        material.name = request.data["name"]
        material.save()
        return material
    except:
        return False

# delete material
def delete_material_service(material_uuid):
    try:
        material = Material.objects.get(uuid=material_uuid)
        material.delete()
        return True
    except:
        return False

"""
Material Stock Service
"""

# list all material stock associate with a store 
def list_material_stock_service(request,store_uuid):
    store = get_store_service(request.user,store_uuid)
    if not store:
        return False
    inventory = MaterialStock.objects.filter(store = store)
    if not inventory:
        return False
    return inventory

# To check if the max_capacity is lower than current capacity, if yes return current capacity else, return max capacity
def check_and_return_valid_max_capacity(max_capacity,current_capacity):
    if max_capacity<current_capacity:
        return current_capacity
    return max_capacity

# create material stock
def create_material_stock_service(request,store_uuid,material_uuid):
    try:
        material = Material.objects.get(uuid=material_uuid)
        store = get_store_service(request.user,store_uuid)
        if material and store:
            material_stock = MaterialStock.objects.create(material = material,store=store,
                                                        current_capacity  = int(request.data["current_capacity"]),
                                                        max_capacity = check_and_return_valid_max_capacity(int(request.data["max_capacity"]),
                                                                                                            int(request.data["current_capacity"])))
            if material_stock:
                return material_stock
    except:
        return False

# update max_capacity of material stock
def update_max_capacity_service(request,store_uuid,material_stock_uuid):
    store = get_store_service(request.user,store_uuid)
    if not store:
        return False
    try:
        material_stock = MaterialStock.objects.get(uuid=material_stock_uuid,store=store)
        material_stock.max_capacity = check_and_return_valid_max_capacity(int(request.data["max_capacity"]),int(material_stock.current_capacity))
        material_stock.save()
        return material_stock
    except:
        return False

# delete material stock        
def delete_material_stock_service(request,store_uuid,material_stock_uuid):
    store = get_store_service(request.user,store_uuid)
    if not store:
        return False
    try:
        material = MaterialStock.objects.get(uuid=material_stock_uuid,store=store)
        material.delete()
        return True
    except:
        return False
    
"""
Material Quantity Service
"""

# create material quantity for a product that is associate with a store 
def create_material_quantity_service(request,store_uuid, material_uuid,product_uuid):
    try:
        material = Material.objects.get(uuid = material_uuid)
        product = get_product_service(request,store_uuid=store_uuid,product_uuid = product_uuid)
        material_quantity = MaterialQuantity.objects.create(ingredient = material, product = product, quantity = request.data["quantity"])
        if material_quantity:
            return material_quantity
        return False
    except:
        return False
    
# create the quantity field of material quantity for a product that is associate with a store 
def update_material_quantity_service(request,store_uuid, material_uuid,product_uuid,material_quantity_uuid):
    try:
        material = Material.objects.get(uuid = material_uuid)
        product = get_product_service(request,store_uuid=store_uuid,product_uuid = product_uuid)
        material_quantity = MaterialQuantity.objects.get(ingredient = material,product=product, uuid = material_quantity_uuid)
        if material_quantity:
            material_quantity.quantity = request.data["quantity"]
            material_quantity.save()
            return material_quantity
        return False
    except:
        return False

# list all material quantity for a product that is associate with a store 
def list_material_quantity_service(request,store_uuid,product_uuid):
    try:
        product = get_product_service(request,store_uuid=store_uuid,product_uuid = product_uuid)
        material_quantity = MaterialQuantity.objects.filter(product = product)
        if material_quantity:
            return material_quantity
        return False
    except:
        return False

# delete a material quantity for a product that is associate with a store 
def delete_material_quantity_service(request,store_uuid, material_uuid,product_uuid,material_quantity_uuid):
    try:
        material = Material.objects.get(uuid = material_uuid)
        product = get_product_service(request,store_uuid=store_uuid,product_uuid = product_uuid)
        material_quantity = MaterialQuantity.objects.get(ingredient = material,product=product, uuid = material_quantity_uuid)
        if material_quantity:
            material_quantity.delete()
            return True
        return False
    except:
        return False

# return the quantity of material and total price to restock a type of material
def check_for_restock(material_stock_uuid):
    try:
        material_stock = MaterialStock.objects.get(uuid =material_stock_uuid)
        # minus the current capacity of material stock using max capacity to get the amount require to restock
        amount_to_restock = material_stock.max_capacity-material_stock.current_capacity
        material = Material.objects.get(uuid = material_stock.material.uuid)
        # times the amount_to_restock with material price to get total price
        price = amount_to_restock*material.price
        return price
    except:
        return None
    
# return retocked material stock or false after a request for restock was made
def request_for_restock(material_stock_uuid):
    try:
        material_stock = MaterialStock.objects.get(uuid = material_stock_uuid)
        amount_restocked = material_stock.max_capacity - material_stock.current_capacity
        material_stock.current_capacity = material_stock.max_capacity
        material_stock.save()
        return amount_restocked
    except:
        return False