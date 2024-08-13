
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Supplier,Bill, Product, Customer, Bank,ProductStock,StockBill,Unit
from .serializers import ProductStockSearchSerializer, StockBillSerializer,SupplierAddSerializer,ProductStockViewSerializer, BillSerializer,ProductSerializer, CustomerSerializer, BankSerializer,UnitSerializer
from django.db.models import Q
from django.db import transaction

# this one adds a new supplier and views allsupplier
@api_view(['GET', 'POST'])
def supplier_list_create(request):
    if request.method == 'GET':
        suppliers = Supplier.objects.all()
        serializer = SupplierAddSerializer(suppliers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SupplierAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



#=============stock ===================
#create new product and view all the available products
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)




#search for adding in table for sale
@api_view(['GET'])
def search_products(request):
    query = request.query_params.get('search', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.none()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

#search products from the stock available. ignores 0 qty products
@api_view(['GET'])
def search_product_stock(request):
    query = request.GET.get('query', '')
    if query:
        stocks = ProductStock.objects.filter(
            quantity__gt=0
        ).filter(
            Q(product__name__icontains=query) 
        )
    else:
        stocks = ProductStock.objects.filter(quantity__gt=0)
    
    serializer = ProductStockSearchSerializer(stocks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#==============stock end=================




#========================billing section=========
#handels the pos billing funtcionality ony post
@api_view(['POST'])
def create_bill(request):
    serializer = BillSerializer(data=request.data)
    if serializer.is_valid():
        bill = serializer.save()

        # Collect items to be deducted
        items_to_deduct = request.data.get('items', [])

        try:
            with transaction.atomic():
                for item in items_to_deduct:
                    product_id = item.get('product')
                    quantity = item.get('quantity')

                    # Fetch all ProductStock entries for the given product
                    product_stocks = ProductStock.objects.filter(product_id=product_id).order_by('date_purchased')

                    total_quantity = sum([product_stock.quantity for product_stock in product_stocks])

                    if quantity > total_quantity:
                        return Response({'error': f'Not enough stock for product {product_id}'}, status=status.HTTP_400_BAD_REQUEST)

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

                # Update the bank balance

                bank = Bank.objects.get(id=bill.payment_method)
                if bank:
                    bank.balance += bill.total_paid
                    bank.save()
                
        except ProductStock.DoesNotExist:
            return Response({'error': 'ProductStock entry not found'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
#view all the bills
@api_view (['GET'])
def bill_list(request):
    if request.method == 'GET':
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)

#========================billing section end=========

#================== stock bill start==================================
#view available product stock quantity 
@api_view(['GET', 'POST'])
def product_stock_list(request):
    if request.method == 'GET':
        stocks = ProductStock.objects.filter(quantity__gt=0)
        serializer = ProductStockViewSerializer(stocks, many=True)
        return Response(serializer.data)
    
    

@api_view(['GET', 'POST'])
def add_or_list_stock(request):
    if request.method == 'POST':
        serializer = StockBillSerializer(data=request.data)
        if serializer.is_valid():
            stock_bill = serializer.save()

            # Optionally, update bank balance if payment is made via bank
            if stock_bill.payment_method:
                bank = Bank.objects.get(id=stock_bill.payment_method)
                if bank:
                    if bank.balance < stock_bill.total_paid:
                        stock_bill.delete()  # Remove the created stock bill
                        return Response({'error': 'Insufficient bank balance'}, status=status.HTTP_400_BAD_REQUEST)
                    bank.balance -= stock_bill.total_paid
                    bank.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        stock_bills = StockBill.objects.all()
        serializer = StockBillSerializer(stock_bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



#================== stock bill end==================================


#create customers and get customers
@api_view(['GET', 'POST'])
def customer_list_create(request):
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#view add update delete all the bank
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def bank_list_create(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                bank = Bank.objects.get(pk=pk)
                serializer = BankSerializer(bank)
                return Response(serializer.data)
            except Bank.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            banks = Bank.objects.all()
            serializer = BankSerializer(banks, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:
            bank = Bank.objects.get(pk=pk)
        except Bank.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BankSerializer(bank, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            bank = Bank.objects.get(pk=pk)
        except Bank.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        bank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#view add update delete all the unit
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def unit_list_create(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                unit = Unit.objects.get(pk=pk)
                serializer = UnitSerializer(unit)
                return Response(serializer.data)
            except Unit.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            units = Unit.objects.all()
            serializer = UnitSerializer(units, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:
            unit = Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UnitSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            unit = Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
