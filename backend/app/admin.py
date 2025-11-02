from django.contrib import admin
from .models import products

all_fields = [field.name for field in products._meta.get_fields() if not field.auto_created]

class ProductsAdmin(admin.ModelAdmin):
    list_display = all_fields  

admin.site.register(products, ProductsAdmin)
