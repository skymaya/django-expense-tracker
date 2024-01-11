from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from .models import (
    User, 
    ExpenseCategory, 
    Expense
)
from django.core.exceptions import ObjectDoesNotExist


class BaseTests(TestCase):
    user = None
    password = 'password'
    username = 'user'
    email = 'example@example.com'

    def setUp(self):
        self.user = User.objects.create(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        self.client = Client()
        self.client.login(username=self.username, password=self.password)


class ExpenseTests(BaseTests):
    category = None

    @classmethod
    def setUpTestData(cls):
        cls.category = ExpenseCategory.objects.create(name='Entertainment',
                                                  slug='entertainment',
                                                  long_description='Stuff you do for fun',
                                                  hex_color='#000000')
        cls.category.save()

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
        path = '/entertainment/'
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
        expense = Expense.objects.get(user__username=self.username)
        self.assertEqual(errors, None)
        self.assertEqual(expense.amount, 12)
        self.assertEqual(expense.description, 'streaming service')
        self.assertEqual(expense.category.slug, 'entertainment')
        self.assertEqual(expense.user.username, self.username)


class AccountTests(BaseTests):
    category = None
    new_email_correct = 'test@example.com'
    new_email_incorrect = 'fdgdfdfvbdfbdb'

    @classmethod
    def setUpTestData(cls):
        cls.category = ExpenseCategory.objects.create(name='Entertainment',
                                                  slug='entertainment',
                                                  long_description='Stuff you do for fun',
                                                  hex_color='#000000')
        cls.category.save()

    def test_change_email_correctly(self):
        """
        Test that it's possible to change a user email correctly
        """
        path = '/account/'
        payload = {
            'new_email': self.new_email_correct,
            'submit': 'changeemail'
        }
        response = self.client.post(path, payload)
        updated_user = User.objects.get(username=self.username)
        self.assertEqual(updated_user.email, self.new_email_correct)

    def test_change_email_incorrectly(self):
        """
        Test that it's impossible to change a user email incorrectly
        """
        path = '/account/'
        payload = {
            'new_email': self.new_email_incorrect,
            'submit': 'changeemail'
        }
        response = self.client.post(path, payload)
        updated_user = User.objects.get(username=self.username)
        self.assertEqual(updated_user.email, self.email)

    def test_delete_account(self):
        """
        Test that deleting a user account works and expense data is also deleted
        """
        expense = Expense.objects.create(
            user=self.user,
            amount=12,
            description='streaming service',
            category=self.category
        )
        path = '/account/'
        payload = {
            'submit': 'deleteaccount'
        }
        response = self.client.post(path, payload)
        with self.assertRaisesMessage(ObjectDoesNotExist, 'User matching query does not exist.'):
            User.objects.get(username=self.username)
        with self.assertRaisesMessage(ObjectDoesNotExist, 'Expense matching query does not exist.'):
            Expense.objects.get(user__username=self.username)
