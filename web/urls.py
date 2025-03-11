from django.urls import path
from web.views import *

urlpatterns = [
    path("", main_view, name="main"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("add/", add_view, name="add"),
    path('delete/<int:book_id>/', delete_view, name='delete'),
    path('edit/<int:book_id>/', edit_view, name='edit'),
]
