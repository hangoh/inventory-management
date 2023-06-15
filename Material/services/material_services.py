from Store.services.store_services import get_store_service,get_product_service
from Store.models import Product
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
def update_material_service(request,material_id):
    try:
        material = Material.objects.get(material_id=material_id)
        material.price = request.data["price"]
        material.name = request.data["name"]
        material.save()
        return material
    except:
        return False

# delete material
def delete_material_service(material_id):
    try:
        material = Material.objects.get(material_id=material_id)
        material.delete()
        return True
    except:
        return False

"""
Material Stock Service
"""

# list all material stock associate with a store 
def list_material_stock_service(request,store_id):
    store = get_store_service(request.user,store_id)
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
def create_material_stock_service(request,store_id,material_id):
    try:
        material = Material.objects.get(material_id=material_id)
        store = get_store_service(request.user,store_id)
        if material and store:
            material_stock = MaterialStock.objects.create(material = material,store=store,
                                                        current_capacity  = int(request.data["current_capacity"]),
                                                        max_capacity = check_and_return_valid_max_capacity(int(request.data["max_capacity"]),
                                                                                                            int(request.data["current_capacity"])))
            if material_stock:
                return material_stock
    except:
        return False

# update max_capacity of materrial stock
def update_max_capacity_service(request,store_id,material_stock_id):
    store = get_store_service(request.user,store_id)
    if not store:
        return False
    try:
        material_stock = MaterialStock.objects.get(id=material_stock_id,store=store)
        material_stock.max_capacity = check_and_return_valid_max_capacity(int(request.data["max_capacity"]),int(material_stock.current_capacity))
        material_stock.save()
        return material_stock
    except:
        return False

# delete material stock        
def delete_material_stock_service(request,store_id,material_stock_id):
    store = get_store_service(request.user,store_id)
    if not store:
        return False
    try:
        material = MaterialStock.objects.get(id=material_stock_id,store=store)
        material.delete()
        return True
    except:
        return False
    
"""
Material Quantity Service
"""

# create material quantity for a product that is associate with a store 
def create_material_quantity_service(request,store_id, material_id,product_id):
    try:
        material = Material.objects.get(material_id = material_id)
        product = get_product_service(request,store_id=store_id,product_id = product_id)
        material_quantity = MaterialQuantity.objects.create(ingredient = material, product = product, quantity = request.data["quantity"])
        if material_quantity:
            return material_quantity
        return False
    except:
        return False
    
# create the quantity field of material quantity for a product that is associate with a store 
def update_material_quantity_service(request,store_id, material_id,product_id,material_quantity_id):
    try:
        material = Material.objects.get(material_id = material_id)
        product = get_product_service(request,store_id=store_id,product_id = product_id)
        material_quantity = MaterialQuantity.objects.get(ingredient = material,product=product, id = material_quantity_id)
        if material_quantity:
            material_quantity.quantity = request.data["quantity"]
            material_quantity.save()
            return material_quantity
        return False
    except:
        return False

# list all material quantity for a product that is associate with a store 
def list_material_quantity_service(request,store_id,product_id):
    try:
        product = get_product_service(request,store_id=store_id,product_id = product_id)
        material_quantity = MaterialQuantity.objects.filter(product = product)
        if material_quantity:
            return material_quantity
        return False
    except:
        return False

# delete a material quantity for a product that is associate with a store 
def delete_material_quantity_service(request,store_id, material_id,product_id,material_quantity_id):
    try:
        material = Material.objects.get(material_id = material_id)
        product = get_product_service(request,store_id=store_id,product_id = product_id)
        material_quantity = MaterialQuantity.objects.get(ingredient = material,product=product, id = material_quantity_id)
        if material_quantity:
            material_quantity.delete()
            return True
        return False
    except:
        return False
