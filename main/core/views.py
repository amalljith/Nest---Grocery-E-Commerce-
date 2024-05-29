from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,Wishlist,Address
from taggit.models import Tag
from django.db.models import Avg, Count
from .forms import ProductReviewForm

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
    # product = get_object_or_404(Product,pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    
    # Getting all reviews related a product
    review = ProductReview.objects.filter(product=product).order_by("-date")
    
    #Getting average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    #product review form
    review_form = ProductReviewForm()
    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user,product=product).count()

        if user_review_count >0:
            make_review = False


    p_image = product.p_images.all()


    context = {
        "make_review":make_review,
        "pro":product,
        "product":products,
        "p_image":p_image,
        "review_form":review_form,
        "average_rating":average_rating,
        "review":review,
        
    }

    return render(request,"core/product-details.html",context)


def tags(request,tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")

    tag = get_object_or_404(Tag, slug =tag_slug)
    products = products.filter(tags__in = [tag])

    context = {
        "products":products,
        "tag":tag
    }

    return render(request,"core/tag.html",context)

def ajax_addreview(request,pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],

    )
    context ={
        'user':user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],

    }
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    return JsonResponse(
        {
            'bool':True,
        'context':context,
        'average_reviews':average_reviews,
        }
    )


