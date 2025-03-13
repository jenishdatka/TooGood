import random
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail

from main.models import MyUser
from .forms import UserRegisterForm
from .models import OTP


def user_profile_view(request):
    return render(request, 'account/user_profile.html')

def user_register_view(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('index')

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')

    form = UserRegisterForm()
    return render (request, template_name='account/user_register.html', context={"form":form})

def generate_otp_code():
    random_code = random.randint(100000, 999999)
    return random_code


def user_login_view(request):
    if request.method =='POST':
        user_email = request.POST['email']
        user_password = request.POST['password']

        user=authenticate(request, username=user_email, password=user_password)

        if user.is_otp:
            if user:
                otp = OTP.objects.create(user=user, code=generate_otp_code())

                send_mail(
                    'Код для входа на сайт',
                    f'Вот код\n{otp.code}',
                    settings.DEFAULT_FROM_EMAIL,
                    ["azbk2004@gmail.com"],
                    fail_silently=False
                )

                messages.error(request,'Неверный логин и/или пароль')

                return render(request, 'account/user_login.html')

            else:
                messages.success(request, 'Вы успешно вошли в систему')
                return redirect('index')

def user_logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('index')

def otp_verification_view(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)

    if request.method == 'POST':
        otp_code = request.POST['otp_code']

        otp = OTP.objects.filter(user=user, if_used=False, code = otp_code).last()

        if otp.is_used:
            otp.save()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('index')

        messages.error(request, 'Неверный код подтверждения')

    return render(request, 'account/otp_verify.html', {"user_id": user_id})

