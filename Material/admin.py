from django.contrib import admin

from .models import Material, MaterialQuantity, MaterialStock

# Register your models here.
admin.site.register(Material)
admin.site.register(MaterialQuantity)
admin.site.register(MaterialStock)
