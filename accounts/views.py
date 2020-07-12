from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from accounts.forms import UserLoginForm

from accounts.forms import UserLoginForm, UserRegistrationForm


def login_view(request):  # вход
    form = UserLoginForm(request.POST or None)  # получение данных с формы
    if form.is_valid():
        data = form.cleaned_data  # получение данных с формы
        email = data.get('email')  # получение email
        password = data.get('password')  # получение password
        user = authenticate(request, email=email, password=password)
        login(request, user)  # аудентификация юзера
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):  # выход
    logout(request)
    return redirect('home')


def register_view(request):  # регистрация
    form = UserRegistrationForm(request.POST or None)  # получение данных с формы
    if form.is_valid():
        new_user = form.save(commit=False)  # приостановление сохранения
        new_user.set_password(form.cleaned_data['password'])  # set_password - шифровка пароля
        new_user.save()  # сохранение
        return render(request, 'accounts/register_done.html',
                      {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})
