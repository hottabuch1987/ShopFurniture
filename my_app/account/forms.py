from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Reviews
from captcha.fields import ReCaptchaField
from django import forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = ReCaptchaField()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с таким именем уже существует')
        elif User.objects.filter(email=email).exists():
            self.add_error('email', 'Пользователь с таким email уже существует')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'captcha')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'avatar')


class ReviewsForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Reviews
        fields = ['name',  'tel', 'captcha']

