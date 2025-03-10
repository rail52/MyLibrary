from datetime import datetime
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from web.forms import RegistrationForm, AuthForm
from .models import Book

User = get_user_model()

@login_required
def main_view(request):
    books = Book.objects.filter(user=request.user)
    return render(request, "web/main.html", {
        "books": books,
        "user": request.user
    })



def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {
        "form": form, "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "web/auth.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main")
