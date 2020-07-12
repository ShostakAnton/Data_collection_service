from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args,
              **kwargs):  # Метод clean() потомка формы. Этот метод может выполнять любую проверку, которая нуждается в одновременном доступе к данным нескольких полей.
        email = self.cleaned_data.get('email').strip()  # strip - это иногнорирование пробелов
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, qs[0].password):  # ф-ция check_password проверяет равен ли
                # полученый пароль, паролю юзера
                raise forms.ValidationError('Пароль не верный!')  # выброс исключения
            user = authenticate(email=email, password=password)  # аудентификация пользователя
            if not user:  # если пользователь не активен
                raise forms.ValidationError('Данный аккаунт отключен')  # выброс исключения
        return super(UserLoginForm, self).clean(*args, **kwargs)
