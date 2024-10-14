from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import NewProductForm, EditProductForm


def browse(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id) 

    if query:
        products = products.filter(name__icontains=query)

    return render (request, 'products/browse.html', {
        'products': products,
        'query': query, 
        'categories': categories, 
        'category_id': int(category_id)

    })


def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[0:3]

    return render(request, 'products/detail.html', {
        'product': product,
        'related_products': related_products
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)

        if form.is_valid():
            Product = form.save(commit=False)
            Product.created_by = request.user
            Product.save()

            return redirect('products:detail', pk=Product.id)
    else:   
        form = NewProductForm()

    return render(request, 'products/form.html', {
        'form': form,
        'title': 'New Product', 
    })

@login_required
def edit(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            return redirect('products:detail', pk=product.id)
    else:   
        form = EditProductForm(instance=Product)

    return render(request, 'products/form.html', {
        'form': form,
        'title': 'Edit Product', 
    })

@login_required
def delete(request, pk):
    products = get_object_or_404(Product, pk=pk, created_by=request.user)
    products.delete()

    return redirect('dashboard:index')