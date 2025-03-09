from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Book(models.Model):
    title = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)


class Author(models.Model):
    name = models.CharField(max_length=64)
    book = models.ManyToManyField(Book)


