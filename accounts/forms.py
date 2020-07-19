from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import City, Language

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


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Введите email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введите пароль ещё раз',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):  # проверка на совпадение двух паролей
        data = self.cleaned_data  # получение информации с введеных форм
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name="slug", required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Город'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), to_field_name="slug", required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Специальность'
    )
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                    label='Получать рассылку?')

    class Meta:
        model = User
        fields = ('city', 'language', 'send_email')


class ContactForm(forms.Form):
    city = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Город'
    )
    language = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Специальность'
    )
    email = forms.EmailField(
        label='Введите email', required=True, widget=forms.EmailInput(
            attrs={'class': 'form-control'})
    )
