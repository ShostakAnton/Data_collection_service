from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from accounts.forms import UserLoginForm


def login_view(request):        # вход
    form = UserLoginForm(request.POST or None)      # получение данных с формы
    if form.is_valid():
        data = form.cleaned_data    # получение данных с формы
        email = data.get('email')   # получение email
        password = data.get('password')     # получение password
        user = authenticate(request, email=email, password=password)
        login(request, user)    # аудентификация юзера
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):       # выход
    logout(request)
    return redirect('home')
