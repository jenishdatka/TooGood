from django.shortcuts import render
from .models import Product

def index_view(request):
    products = Product.objects.filter(is_active=True)

    return render(request=request, template_name='main/index.html', context={'products': products})
