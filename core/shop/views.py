
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Supplier, Product, Customer, Sale, Bank,ProductStock
from .serializers import SupplierSerializer,ProductStockViewSerializer, BillSerializer,ProductSerializer, CustomerSerializer, SaleSerializer, BankSerializer,ProductStockSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import transaction


@api_view(['GET', 'POST'])
def supplier_list_create(request):
    if request.method == 'GET':
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def product_list_create(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



#=============stock ===================

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




#add of view product available in stock
@api_view(['GET', 'POST'])
def product_stock_list(request):
    if request.method == 'GET':
        stocks = ProductStock.objects.all()
        serializer = ProductStockViewSerializer(stocks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductStockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    


#search for adding in table for sale
@api_view(['GET'])
def search_products(request):
    query = request.GET.get('query', '')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(unit__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    return Response([])





@api_view(['POST'])
def create_bill(request):
    with transaction.atomic():
        bill_serializer = BillSerializer(data=request.data)
        
        if bill_serializer.is_valid():
            # Save the bill
            bill = bill_serializer.save()
            
            sales_data = request.data.get('sales', [])
            for sale_data in sales_data:
                product_id = sale_data['product']
                quantity = sale_data['quantity']
                
                # Validate and update stock
                product_stock = ProductStock.objects.filter(product_id=product_id).first()
                if product_stock and product_stock.quantity >= quantity:
                    product_stock.quantity -= quantity
                    product_stock.save()
                    
                    # Create Sale
                    sale_data['bill'] = bill.id
                    sale_serializer = SaleSerializer(data=sale_data)
                    if sale_serializer.is_valid():
                        sale_serializer.save()
                    else:
                        return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response(bill_serializer.data, status=status.HTTP_201_CREATED)
        return Response(bill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)








@api_view(['GET', 'POST'])
def sale_list(request):
    if request.method == 'GET':
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
#==============stock end=================









# @api_view(['GET', 'POST'])
# def supplier_product_list_create(request):
#     if request.method == 'GET':
#         supplier_products = SupplierProduct.objects.all()
#         serializer = SupplierProductSerializer(supplier_products, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = SupplierProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# @api_view(['GET'])
# def product_search(request):
#     query = request.query_params.get('q', None)
#     if query:
#         products = Product.objects.filter(name__icontains=query)
#     else:
#         products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# @api_view(['GET', 'POST'])
# def product_stock_list(request):
#     if request.method == 'GET':
#         product_stocks = ProductStock.objects.all()
#         serializer = ProductStockSerializer(product_stocks, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = ProductStockSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









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

@api_view(['GET', 'POST'])
def sale_list_create(request):
    if request.method == 'GET':
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def bank_list_create(request):
    if request.method == 'GET':
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
