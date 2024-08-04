from django.db import models

# Create your models here.
from django.contrib.auth.models import User

#make a abstract class for BasePeople
class BasePeople(models.Model):
    name = models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=15,null=True)
    contact_info = models.TextField(null=True)

    class Meta:
        abstract = True


class Supplier(BasePeople):
    def __str__(self):
        return self.name
    

    
class Customer(BasePeople):
    def __str__(self):
        return self.name
    



class Product(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)  # e.g., 'kg', 'liter', 'pc', etc.
    selling_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2 ,null =True)

    def __str__(self):
        return self.name
    

class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    supplier_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    date_purchased = models.DateField()

    def __str__(self):
        return f'{self.product.name} from {self.supplier.name} on {self.date_purchased}'


#------------------bill---------------- 

class Bill(models.Model):
    customer_phone = models.CharField(max_length=20, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_profit_or_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateField(null=True)

    def __str__(self):
        return f"Bill #{self.id} - {self.customer_phone}"



class SaleItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=True)
    selling_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
#------------------bill end----------------      






#unused

class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name
