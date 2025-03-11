from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from web.forms import RegistrationForm, AuthForm, AddBookForm, EditBookForm
from .models import Book, Author

User = get_user_model()


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


@login_required
def main_view(request):
    books = Book.objects.filter(user=request.user)
    return render(request, "web/main.html", {
        "books": books,
        "user": request.user
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


@login_required
def add_view(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            # Создаем книгу и привязываем её к текущему пользователю
            book = Book.objects.create(
                title=form.cleaned_data['title'],
                user=request.user
            )
            # Создаем или находим автора
            author_name = form.cleaned_data['author_name']
            author, created = Author.objects.get_or_create(name=author_name)
            # Связываем книгу с автором
            book.author_set.add(author)
            return redirect('main')  # Перенаправляем на страницу со списком книг
    else:
        # Если это GET-запрос, создаем пустую форму
        form = AddBookForm()

        # Передаем форму в шаблон
    return render(request, 'web/add.html', {
        'form': form
    })


@login_required
def delete_view(request, book_id):
    # Находим книгу по ID и проверяем, что она принадлежит текущему пользователю
    book = get_object_or_404(Book, id=book_id, user=request.user)
    # Удаляем книгу
    book.delete()
    # Перенаправляем на страницу со списком книг
    return redirect('main')


@login_required
def edit_view(request, book_id):
    # Находим книгу по ID и проверяем, что она принадлежит текущему пользователю
    book = get_object_or_404(Book, id=book_id, user=request.user)

    if request.method == 'POST':
        # Если форма отправлена, обрабатываем данные
        form = EditBookForm(request.POST, instance=book)

        if form.is_valid():
            # Обновляем книгу
            book = form.save(commit=False)
            book.user = request.user  # Привязываем книгу к текущему пользователю
            book.save()

            # Обновляем автора
            author_name = form.cleaned_data['author_name']
            author, created = Author.objects.get_or_create(name=author_name)
            book.author_set.clear()  # Удаляем старых авторов
            book.author_set.add(author)  # Добавляем нового автора

            return redirect('main')  # Перенаправляем на страницу со списком книг
    else:
        # Если это GET-запрос, заполняем форму текущими данными
        initial_data = {
            'title': book.title,
            'author_name': book.author_set.first().name if book.author_set.exists() else ''
        }
        form = EditBookForm(instance=book, initial=initial_data)

    return render(request, 'web/edit.html', {'form': form, 'book': book})
