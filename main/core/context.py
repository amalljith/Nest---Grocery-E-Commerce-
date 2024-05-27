from .models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,Wishlist,Address

def default(request):
    category = Category.objects.all()

    return {
        "categories":category
    }