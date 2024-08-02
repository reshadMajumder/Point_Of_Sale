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

class Product(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)  # e.g., 'kg', 'liter', 'pc', etc.
    selling_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2 ,null =True)

    def __str__(self):
        return self.name
    





class ProductStock(models.Model):
    # PAYMENT_METHOD_CHOICES = [
    #     ('CASH', 'Cash'),
    #     ('BANK', 'Bank'),
    # ]

    # PAYMENT_STATUS_CHOICES = [
    #     ('PAID', 'Paid'),
    #     ('PARTIAL', 'Partial Paid'),
    #     ('DUE', 'Due'),
    # ]

    # supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # purchase_date = models.DateField()
    # quantity = models.DecimalField(max_digits=10, decimal_places=2)
    # buying_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    # selling_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    # total_paid_to_supplier = models.DecimalField(max_digits=10, decimal_places=2)
    # payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES)
    # payment_status = models.CharField(max_length=7, choices=PAYMENT_STATUS_CHOICES)

    # def __str__(self):
    #     return f"{self.product.name} from {self.supplier.name}"

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    supplier_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    date_purchased = models.DateField()

    def __str__(self):
        return f'{self.product.name} from {self.supplier.name} on {self.date_purchased}'





    

class Customer(BasePeople):
    def __str__(self):
        return self.name






class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True ,null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def __str__(self):
        return f'Bill {self.id} - {self.customer.phone_number}'



class Sale(models.Model):
    bill = models.ForeignKey(Bill, related_name='sales', on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=True)
    selling_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def __str__(self):
        return f'Sale of {self.product.name} in {self.bill.id}'
        







class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name
