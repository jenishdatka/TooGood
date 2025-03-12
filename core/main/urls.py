from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    #Product
    path('product/<int:product_id>', views.product_detail_view, name='product_detail'),
    path('product/create/', views.product_create_view, name='product_create'),
    path('product/update/<int:product_id>', views.product_update_view, name='product_update'),
    path('product/<int:product_id>/payment/create', views.product_payment_create_view, name='product_payment_create'),
    #Rating
    path('rating/create/<int:product_id>', views.rating_create_view, name='rating_create'),
    path('rating_answer/create/<int:rating_id>', views.rating_answer_create_view, name='rating_answer_create'),
    #User
    path('profile/', views.user_profile_view, name = 'user_profile'),

]