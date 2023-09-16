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
    

class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ("Open", "Open"),
        ("Staff Replied", "Staff Replied"),
        ("User Replied", "User Replied"),
        ("Closed", "Closed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True, verbose_name='Date')
    subject = models.CharField(max_length=255, verbose_name='Subject')
    body = models.TextField(verbose_name='Ticket Body')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="Open")

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.subject
    

class SupportTicketReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='replies')
    date = models.DateField(auto_now=True, verbose_name='Date')
    body = models.TextField(verbose_name='Ticket Body')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'Reply to {self.ticket.subject}'
    
    def save(self, *args, **kwargs):
        if self.user.is_staff:
            self.ticket.status = 'Staff Replied'
            self.ticket.save()
        super(SupportTicketReply, self).save(*args, **kwargs)