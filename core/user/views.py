from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib import messages

from core.user.forms import UserRegisterForm


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


def user_login_view(request):
    if request.method =='POST':
        user_email = request.POST['email']
        user_password = request.POST['password']

        user=authenticate(request, username=user_email, password=user_password)

        if user:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('index')
        messages.error(request,'Неверный логин и/или пароль')

    return render(request, 'account/user_login.html')

def user_logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('index')
