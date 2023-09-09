from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    long_description = models.TextField()
    slug = models.CharField(max_length=255)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    amount = models.FloatField(default=0)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ['date']