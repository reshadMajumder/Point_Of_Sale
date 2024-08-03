from django.contrib import admin
from .models import Supplier, Product, Customer,Bill, SaleItem, ProductStock

# Register your models here.

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(SaleItem)
admin.site.register(ProductStock)
admin.site.register(Bill)