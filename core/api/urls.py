from django.urls import path
from authentication.views import login_view,logout_view
from shop.views import create_bill,product_list,search_product_stock, supplier_list_create, sale_list_create, bank_list_create,product_stock_list

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    path('suppliers/', supplier_list_create, name='supplier_list_create'),
    path('products/', product_list, name='product-list'),
    path('stocks/', product_stock_list,name='product-stock-list'),
    path('stocks/search/', search_product_stock, name='search-product-stock'),

    # path('search-products/', search_products, name='search_products'),
    path('bills/', create_bill, name='create_bill'),

]



#path('products/', product_list_create, name='product_list_create'),
    # # path('supplier-products/', supplier_product_list_create, name='supplier_product_list_create'),
    # path('customers/', customer_list_create, name='customer_list_create'),
    # path('sales/', sale_list_create, name='sale_list_create'),
    # path('banks/', bank_list_create, name='bank_list_create'),
      # path('product-stock/', product_stock_list, name='product-stock-list'),
    # path('sales/', sale_list),
