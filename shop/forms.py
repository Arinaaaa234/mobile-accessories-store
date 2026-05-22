from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import NewsletterSubscriber, Order, Rating


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["full_name", "email"]
        labels = {"full_name": "Ім'я", "email": "Email"}


class RatingForm(forms.ModelForm):
    score = forms.ChoiceField(
        label="Оцінка",
        choices=[(value, f"{value}") for value in range(1, 6)],
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Rating
        fields = ["score", "comment"]
        labels = {"comment": "Коментар"}


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "email", "phone", "address"]
        labels = {
            "customer_name": "Ім'я",
            "email": "Email",
            "phone": "Телефон",
            "address": "Адреса доставки",
        }


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email")


class PasswordResetConfirmForm(forms.Form):
    email = forms.EmailField(label="Email")
    code = forms.CharField(label="Код з листа", max_length=8)
    new_password = forms.CharField(label="Новий пароль", widget=forms.PasswordInput)
