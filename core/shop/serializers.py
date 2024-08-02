from rest_framework import serializers
from .models import Supplier, Product,  Customer, Sale,Bill, Bank,ProductStock

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:

        model = Product
        fields = '__all__'


class ProductStockViewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), source='supplier', write_only=True)

    class Meta:
        model = ProductStock
        fields = ['id', 'product', 'supplier', 'quantity', 'supplier_price_per_unit', 'date_purchased', 'product_id', 'supplier_id']

class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ['product', 'supplier', 'quantity', 'supplier_price_per_unit', 'date_purchased']

# class ProductStockSerializer(serializers.ModelSerializer):
#     supplier_name = serializers.CharField(source='supplier.name', read_only=True)
#     product_name = serializers.CharField(source='product.name', read_only=True)
#     class Meta:
#         model = ProductStock
#         fields = [
#             'id', 'supplier', 'supplier_name', 'product', 'product_name', 
#             'purchase_date', 'quantity', 'buying_price_per_unit', 'selling_price_per_unit', 
#             'total_paid_to_supplier', 'payment_method', 'payment_status'
#         ]







# class SupplierProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SupplierProduct
#         fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['phone_number', 'name']


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['product', 'quantity', 'selling_price_per_unit']

class BillSerializer(serializers.ModelSerializer):
    sales = SaleSerializer(many=True)

    class Meta:
        model = Bill
        fields = ['customer', 'total_amount', 'sales']





class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'
