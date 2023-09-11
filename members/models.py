from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    email = models.EmailField(unique=True)


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255)
    long_description = models.TextField()
    slug = models.CharField(max_length=255)
    hex_color = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    amount = models.FloatField(default=0)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.description
    

class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=255)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.subject
    

class SupportTicketReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='replies'),
    date = models.DateField(auto_now=True)
    body = models.TextField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'Reply to {self.ticket.subject}'