from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.core.validators import validate_email


class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[validate_email])


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    long_description = models.TextField(verbose_name='Description')
    slug = models.CharField(max_length=255, verbose_name='Slug')
    hex_color = models.CharField(max_length=255, verbose_name='Hex Color')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today, verbose_name='Date')
    amount = models.FloatField(default=0, verbose_name='Amount')
    description = models.CharField(max_length=255, verbose_name='Description')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.description
