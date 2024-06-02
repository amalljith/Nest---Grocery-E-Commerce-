from .models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,Wishlist,Address
from django.db.models import Min, Max
def default(request):
    category = Category.objects.all()
    vendor = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"),Max("price"))
    try:
      address = Address.objects.get(user=request.user)

    except:
       address = None
    



    return {
        "categories":category,
        "address":address,
        "vendors":vendor,
        "min_max_price":min_max_price,
    }