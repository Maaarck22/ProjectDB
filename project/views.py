# project/views.py

from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Products

def home(request):
    return render(request, 'project/home.html')
def product_list(request):
    products = Products.objects.all()
    return render(request, 'project/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'project/product_form.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    return render(request, 'project/product_detail.html', {'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'project/delete_product.html', {'product': product})

def product_update(request, pk):
    product = get_object_or_404(Products, ProductID=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.ProductID)
    else:
        form = ProductForm(instance=product)
    return render(request, 'project/product_form.html', {'form': form})




