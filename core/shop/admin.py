from django.contrib import admin
from .models import Supplier, Product, Customer, Sale, ProductStock

# Register your models here.

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Sale)
admin.site.register(ProductStock)