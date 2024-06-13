from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,Wishlist,Address
from taggit.models import Tag
from django.db.models import Avg, Q
from .forms import ProductReviewForm
from django.template.loader import render_to_string

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
        "p":product,
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


def search_view(request):
    if request.method == "GET":
            products = request.GET['searched']

            products = Product.objects.filter(Q(title__icontains=products) | Q(description__icontains=products))

            context = {
                
                "products": products
            }

            return render(request,"core/search.html",context)




def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()


    data = render_to_string("core/ajax/product-list.html",{"products":products})
    return JsonResponse({"data":data})




def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title' : request.GET['title'],
        'qty' : request.GET['qty'],
        'price' : request.GET['price'],
        'image' : request.GET['image'],
        'pid' : request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product
    
    return JsonResponse({"data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj'])})



def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * int(item['price'])
        return render(request,"core/cart.html",({"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount}))
    else:
        return render(request,"core/cart.html",{"cart_data":'','totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * int(item['price'])

    context = render_to_string("core/ajax/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    
    

def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * int(item['price'])

    context = render_to_string("core/ajax/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    




def checkout(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * int(item['price'])

        return render(request,"core/checkout.html",({"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount}))
