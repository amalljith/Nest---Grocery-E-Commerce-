from .models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,Wishlist,Address

def default(request):
    category = Category.objects.all()
    address = Address.objects.get(user=request.user)

    return {
        "categories":category,
        "address":address,
    }