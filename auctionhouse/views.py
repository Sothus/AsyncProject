from django.contrib.auth    import authenticate, login
from django.shortcuts       import render, get_object_or_404
from django.http            import HttpResponse
from .models                import Category, Product
from .forms                 import LoginForm

def home_page(request):
    return render(request, 'base.html')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if(category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'product/detail.html', {'product': product})
