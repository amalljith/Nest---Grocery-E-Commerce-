from django.urls import path
from . import views 

app_name = "core"
urlpatterns = [
    #Homepage
    path('',views.home,name='home'),

    #Productpage
    path('products/',views.product_list,name='product_list'),
    path('product/details/<pid>',views.product_details,name='product_details'),

    #Category
    path('categories/',views.category_list,name='category_list'),
    path('categories/list/<cid>',views.category_product_list,name='category_product_list'),

    #Vendor
    path('vendors/',views.vendor_list,name='vendor_list'),
    path('vendors/<vid>',views.vendor_product_list,name='vendor_product_list'),
    
    #Tags
    path('product/tag/<slug:tag_slug>',views.tags,name='tags'),

    #add review

    path('add-review/<pid>/',views.ajax_addreview,name='addreview')

]
