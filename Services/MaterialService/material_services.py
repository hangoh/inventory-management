
from Services.AccountService import account_services
from Material.models import Material_Stock,Material

def list_product_service(request,store_id):
    store = account_services.get_store(request.user,store_id)
    if not store:
        return False
    product = store.products.all()
    if not product:
        return False
    return product

def list_material_service():
    material = Material.objects.all()
    if not material:
        return False
    return material

def list_material_stock_service(request,store_id):
    store = account_services.get_store(request.user,store_id)
    if not store:
        return False
    inventory = Material_Stock.objects.filter(store = store)
    if not inventory:
        return False
    return inventory
