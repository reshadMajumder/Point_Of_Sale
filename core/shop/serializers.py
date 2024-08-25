from rest_framework import serializers
from .models import Supplier,SaleItem,Transaction, Product,Asset,  Customer,Bill, Bank,ProductStock,StockBill,Unit



class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']
class SupplierAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields ='__all__'

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
        fields = '__all__'


        

class ProductStockSearchSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = ProductStock
        fields = ['id', 'product', 'supplier', 'quantity', 'supplier_price_per_unit', 'date_purchased']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['phone_number', 'name']

#=========================POS billing===============
class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Bill
        fields = '__all__'
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        bill = Bill.objects.create(**validated_data)
        for item_data in items_data:
            SaleItem.objects.create(bill=bill, **item_data)
        return bill

#=========================POS billing end===============

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'



#============stock bill ============




class StockBillSerializer(serializers.ModelSerializer):
    items = ProductStockSerializer(many=True)

    class Meta:
        model = StockBill
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        stock_bill = StockBill.objects.create(**validated_data)
        for item_data in items_data:
            # Remove 'stock_bill' from item_data if it exists
            item_data.pop('stock_bill', None)
            ProductStock.objects.create(stock_bill=stock_bill, **item_data)
        return stock_bill




#============stock bill end===========


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'




#=============assets ==============
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
class ViewTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        depth=2
        model = Transaction
        fields = '__all__'



#==========liability update===============
class LiabilityBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'total_paid', 'total_due']  # Only allow these fields to be updated


#==========================update bill======================

class BillUpdateSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Bill
        fields = '__all__'

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        previous_paid = instance.total_paid  # Store the previous total_paid value

        # Update bill fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        current_items = {item.id: item for item in instance.items.all()}
        updated_items = []

        for item_data in items_data:
            item_id = item_data.get('id')
            quantity = item_data.get('quantity')
            if item_id and item_id in current_items:
                item = current_items.pop(item_id)

                # Check if quantity has changed and adjust stock
                if item.quantity != quantity:
                    self._update_stock(item, quantity)

                # Update existing item
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
                updated_items.append(item)
            else:
                # Ensure the bill is not passed as a duplicate argument
                new_item_data = {**item_data}
                new_item_data.pop('bill', None)  # Remove 'bill' from item_data if it exists
                new_item = SaleItem.objects.create(bill=instance, **new_item_data)
                self._deduct_stock(new_item)  # Deduct stock for newly added item
                updated_items.append(new_item)

        # Remove items that were not included in the update
        for item in current_items.values():
            self._restore_stock(item)  # Restore stock for removed items
            item.delete()

        # Adjust the bank balance if total_paid was updated
        if instance.total_paid != previous_paid:
            self._adjust_bank_balance(instance, previous_paid)

        return instance

    def _update_stock(self, item, new_quantity):
        # Adjust stock based on the difference between old and new quantities
        difference = new_quantity - item.quantity

        if difference > 0:
            # Deduct additional quantity
            self._deduct_stock(item, difference)
        elif difference < 0:
            # Restore the difference in quantity
            self._restore_stock(item, -difference)

    def _deduct_stock(self, item, quantity=None):
        # Deduct stock quantity (used for newly added items or when quantity increases)
        if quantity is None:
            quantity = item.quantity
        product_stocks = ProductStock.objects.filter(product_id=item.product_id).order_by('date_purchased')

        for product_stock in product_stocks:
            if quantity <= 0:
                break
            if product_stock.quantity > 0:
                if product_stock.quantity >= quantity:
                    product_stock.quantity -= quantity
                    product_stock.save()
                    quantity = 0
                else:
                    quantity -= product_stock.quantity
                    product_stock.quantity = 0
                    product_stock.save()

    def _restore_stock(self, item, quantity=None):
        # Restore stock quantity (used for removed items or when quantity decreases)
        if quantity is None:
            quantity = item.quantity
        product_stocks = ProductStock.objects.filter(product_id=item.product_id).order_by('-date_purchased')

        for product_stock in product_stocks:
            if quantity <= 0:
                break
            product_stock.quantity += quantity
            product_stock.save()
            quantity = 0

    def _adjust_bank_balance(self, bill, previous_paid):
        bank = Bank.objects.get(id=bill.payment_method)
        if bank:
            bank.balance += (bill.total_paid - previous_paid)
            bank.save()


#==========================update bill end======================
#==========================search saleitem======================
class SearchSaleItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) 
    class Meta:
        model = SaleItem
        fields = '__all__'


class SearchBillSerializer(serializers.ModelSerializer):
    items = SearchSaleItemSerializer(many=True)

    class Meta:
        model = Bill
        fields = '__all__'
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        bill = Bill.objects.create(**validated_data)
        for item_data in items_data:
            SaleItem.objects.create(bill=bill, **item_data)
        return bill
