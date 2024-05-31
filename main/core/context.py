from .models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,Wishlist,Address

def default(request):
    category = Category.objects.all()
    vendor = Vendor.objects.all()
    try:
      address = Address.objects.get(user=request.user)

    except:
       address = None
    



    return {
        "categories":category,
        "address":address,
        "vendors":vendor,
    }