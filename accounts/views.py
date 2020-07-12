from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib import messages

User = get_user_model()

from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm


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
        messages.success(request, "Пользователь добавлен в систему")
        return render(request, 'accounts/register_done.html',
                      {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    if request.user.is_authenticated:  # проверка на аудентивицырованого пользователя
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)  # получение данных с форм
            if form.is_valid():
                data = form.cleaned_data  # получение данных с форм
                user.city = data['city']  # город равен городу полученого с формы
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данные сохраненны.')
                return redirect('accounts:update')

        form = UserUpdateForm(
            initial={'city': user.city, 'language': user.language,
                     'send_email': user.send_email})  # оставить настройки какие были
        return render(request, 'accounts/update.html', {'form': form})
    else:
        return redirect('accounts:login')


def delete_view(request):  # удаление
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)       # получение записи из модели пользователя
            qs.delete()
            messages.error(request, 'Пользователь удален :(')
    return redirect('home')
