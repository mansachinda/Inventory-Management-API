from django.shortcuts import render, redirect
from products.models import Category, Product
from .forms import SignupForm

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'core/index.html',  {
        'categories': categories,
        'products': products,
    })

def contact (request):
    return render(request, 'core/contact.html',)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:

        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })