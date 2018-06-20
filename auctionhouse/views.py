from django.contrib.auth                import authenticate, login
from django.shortcuts                   import render, get_object_or_404, redirect
from django.http                        import HttpResponse
from django.urls                        import reverse
from .models                            import Category, Product
from .forms                             import LoginForm
from django.contrib.auth.decorators     import login_required

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


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username = cd['username'],
                                password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/product_list/")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "login.html", {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'dashboard.html',
                  {'section': 'dashboard'})
