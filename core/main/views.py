from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg

from .models import Product, Rating, RatingAnswer, PaymentMethod
from .forms import ProductCreateForm, ProductUpdateForm

def index_view(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'main/index.html', {'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_update_form = ProductUpdateForm(instance=product)
    product_comments = Rating.objects.filter(product=product)
    rating_avg = product_comments.aggregate(Avg('count'))['count__avg']
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id) if product.category else Product.objects.none()

    return render(request, 'main/product_detail.html', {
        'product': product,
        'similar_products': similar_products,
        "product_update_form": product_update_form,
        "product_comments": product_comments,
        "rating_avg": rating_avg
    })

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
    return render(request, 'main/product_create.html', {'form': form})

def product_update_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены')
            return redirect('product_detail', product_id)
    else:
        form = ProductUpdateForm(instance=product)

    return render(request, 'main/product_update.html', {'form': form, 'product': product})

def rating_create_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_authenticated:
        messages.error(request, 'Только для зарегистрированных пользователей.')
        return redirect('product_detail', product_id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        try:
            count = int(request.POST.get('rating', 0))
        except ValueError:
            messages.error(request, 'Неверное значение рейтинга.')
            return redirect('product_detail', product_id)

        rating = Rating(user=request.user, product=product, count=count, comment=comment)
        rating.save()
        messages.success(request, 'Благодарим вас за отзыв!')
        return redirect('product_detail', product_id)

def rating_answer_create_view(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)

    if not rating.product.user or rating.product.user != request.user:
        messages.error(request, 'Нет доступа')
        return redirect('product_detail', rating.product.id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        rating_answer = RatingAnswer(user=request.user, rating=rating, comment=comment)
        rating_answer.save()
        messages.success(request, 'Успешно отправлено.')
        return redirect('product_detail', rating.product.id)

def user_profile_view(request):
    return render(
        request=request,
        template_name='main/user_profile.html'
    )
def product_payment_create_view(request, product_id):
    product = get_object_or_404(Product, product_id)
    seller_payment_methods = PaymentMethod.objects.filter(user=product.user)

    return render(
        request=request,
        template_name='main/product_payment.html',
        context ={ "seller_payment_methods": seller_payment_methods }
    )