from django.shortcuts import render
from .models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,Wishlist,Address


def home(request):
    products = Product.objects.all()

    context ={"products":products}
    return render(request,"core/index.html",context)


def product_list(request):
    products = Product.objects.filter(product_status="published")

    context ={"products":products}
    return render(request,"core/product-list.html",context)



def category_list(request):
    category = Category.objects.all()

    context ={"category":category}
    return render(request,"core/category-list.html",context)


def category_product_list(request,cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published",category=category)

    context ={"category":category,
              "products":products
              }
    return render(request,"core/category-product-list.html",context)


def vendor_list(request):
    vendors = Vendor.objects.all()
    context = {"vendors":vendors}

    return render(request,'core/ventor_list.html',context)


def vendor_product_list(request,vid):
    vendors = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendors,product_status="published")
    context = {"vendors":vendors,
               "products":products}

    return render(request,'core/vendor-product-list.html',context)


def product_details(request,pid):
    
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    context = {
        "pro":product,
        "p_image":p_image,
        
    }

    return render(request,"core/product-details.html",context)