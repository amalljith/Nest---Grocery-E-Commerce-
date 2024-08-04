from .models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,Wishlist,Address
from django.db.models import Min, Max
from django.contrib import messages



def default(request):
    category = Category.objects.all()
    vendor = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"),Max("price"))

    try:
       wishlist = Wishlist.objects.filter(user=request.user)

    except:
       wishlist = 0
      #  messages.warning(request,"You need to login before accessing your wishlist.")



    try:
      address = Address.objects.get(user=request.user)

    except:
       address = None
    



    return {
        "categories":category,
        "wishlist":wishlist,
        "address":address,
        "vendors":vendor,
        "min_max_price":min_max_price,
    }