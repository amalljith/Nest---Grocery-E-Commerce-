from django.urls import path
from . import views 

app_name = "core"
urlpatterns = [
    path('',views.home,name='home'),
    path('products/',views.product_list,name='product_list'),
    path('categories/',views.category_list,name='category_list'),
    path('categories/list/<cid>',views.category_product_list,name='category_product_list'),
    path('vendors/',views.vendor_list,name='vendor_list'),
    path('vendors/<vid>',views.vendor_product_list,name='vendor_product_list'),
    path('product-details/<pid>',views.product_details,name='product_details'),

]
