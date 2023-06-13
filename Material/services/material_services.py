from Store.services.store_services import get_store_service
from Material.models import Material_Stock,Material

def list_material_service(request,store_id):
    store = get_store_service(request.user,store_id)
    if not store:
        return False
    material = Material.objects.filter(store=store)
    if not material:
        return False
    return material   

def update_material_service(request,store_id,material_id):
    store = get_store_service(request.user,store_id)
    if not store:
        return False
    try:
        material = Material.objects.get(material_id=material_id)
        material.price = request.data["price"]
        material.name = request.data["name"]
        material.save()
        return material
    except:
        return False
    
def delete_material_service(request,store_id,material_id):
    store = get_store_service(request.user,store_id)
    if not store:
        return False
    try:
        material = Material.objects.get(material_id=material_id,store=store)
        material.delete()
        return True
    except:
        return False
    
def list_material_stock_service(request,store_id):
    store = get_store_service(request.user,store_id)
    if not store:
        return False
    inventory = Material_Stock.objects.filter(store = store)
    if not inventory:
        return False
    return inventory

def update_max_capacity_service(request,store_id,material_stock_id):
    store = get_store_service(request.user,store_id)
    if not store:
        return False
    try:
        material_stock = Material_Stock.objects.get(id=material_stock_id,store=store)
        material_stock.max_capacity = request.data["max_capacity"]
        material_stock.save()
        return material_stock
    except:
        return False
    
def delete_material_stock_service(request,store_id,material_stock_id):
    store = get_store_service(request.user,store_id)
    if not store:
        return False
    try:
        material = Material_Stock.objects.get(id=material_stock_id,store=store)
        material.delete()
        return True
    except:
        return False
