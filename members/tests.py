import datetime

from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from .models import User, ExpenseCategory, Expense
from django.db import IntegrityError


class MembersTests(TestCase):
    password = 'password'
    username = 'user'
    email = 'example@example.com'

    def setUp(self):
        user = User.objects.create(username=self.username, email=self.email)
        user.set_password(self.password)
        user.save()

        category = ExpenseCategory.objects.create(name='Entertainment',
                                                  slug='entertainment',
                                                  long_description='Stuff you do for fun',
                                                  hex_color='#000000')
        category.save()

        self.client = Client()
        self.client.login(username=self.username, password=self.password)

    def test_category_slug_response_code(self):
        """
        Test that certain paths return the expected response code
        """
        # undefined category should be 404
        cat_response1 = self.client.get(reverse("expense_category", kwargs={'slug': 'sdfsdvsvbdrvd'}))
        self.assertEqual(cat_response1.status_code, 404)
        cat_response2 = self.client.get(reverse("expense_category", kwargs={'slug': 'entertainment'}))
        self.assertEqual(cat_response2.status_code, 200)

    def test_add_expense_correctly(self):
        """
        Test that it is possible to add an expense correctly
        """
        path = '/members/entertainment/'
        payload = {
            'amount': '12',
            'description': 'streaming service',
            'submit': 'add'
        }
        response = self.client.post(path, payload)
        try:
            errors = response.context['errors']
        except TypeError:
            errors = None
        expense = Expense.objects.get(
            user__username=self.username,
            amount=12,
            description='streaming service',
            category__slug='entertainment'
        )
        self.assertEqual(errors, None)
        self.assertEqual(expense.amount, 12)
        self.assertEqual(expense.description, 'streaming service')
        self.assertEqual(expense.category.slug, 'entertainment')
        self.assertEqual(expense.user.username, self.username)