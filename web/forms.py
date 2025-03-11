from django import forms
from django.contrib.auth import get_user_model
from .models import Book
User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class AddBookForm(forms.Form):
    title = forms.CharField(max_length=64, label="Название книги")  # Поле для названия книги
    author_name = forms.CharField(max_length=64, label="Автор")

class EditBookForm(forms.ModelForm):
    author_name = forms.CharField(max_length=64, label="Автор")  # Поле для имени автора

    class Meta:
        model = Book
        fields = ['title']  # Поле для названия книги