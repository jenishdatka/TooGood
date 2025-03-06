from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductCreateForm, ProductUpdateForm

def index_view(request):
    products = Product.objects.filter(is_active=True)

    return render(request,template_name='main/index.html', context={'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_update_form= ProductUpdateForm()

    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)

    return render(request=request,
                  template_name='main/product_detail.html',
                  context = {'product':product,'similar_products':similar_products,
                             "product_update_form": product_update_form})

def product_create_view(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product_object = form.save(commit=False)
            product_object.user = request.user
            product_object.save()

            messages.success(request, 'Успешно создано!')
            return redirect('index')
    else:
        form = ProductCreateForm()
    return render(request, 'main/product_create.html', context={'form': form})

def product_update_view(request, product_id):
    return render(
        request=request,
        template_name='main/product_update_modal.html'
    )

