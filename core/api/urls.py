from django.urls import path
from authentication.views import login_view,logout_view
from shop.views import create_bill,product_list,sale_list,search_products, supplier_list_create, product_list_create, customer_list_create, sale_list_create, bank_list_create,product_stock_list

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # path('product-stock/', product_stock_list, name='product-stock-list'),


    path('suppliers/', supplier_list_create, name='supplier_list_create'),
    #path('products/', product_list_create, name='product_list_create'),
    # # path('supplier-products/', supplier_product_list_create, name='supplier_product_list_create'),
    # path('customers/', customer_list_create, name='customer_list_create'),
    # path('sales/', sale_list_create, name='sale_list_create'),
    # path('banks/', bank_list_create, name='bank_list_create'),
    path('products/', product_list, name='product-list'),
    path('stocks/', product_stock_list,name='product-stock-list'),
    path('sales/', sale_list),
    path('search-products/', search_products, name='search_products'),
    path('bills/', create_bill, name='create_bill'),

]
