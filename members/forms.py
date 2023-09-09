from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Expense
import re


class ExpenseForm(forms.ModelForm):
    
    class Meta:
        model = Expense
        fields = ['amount', 'description']


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=100, 
        help_text='Required. Only alphanumeric characters allowed.'
    )
    email = forms.EmailField(
        max_length=254, 
        help_text='Required. A valid email address.'
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Required. Choose a secure password.',
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text='Required. Verify your password.',
    )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = cleaned_data.get('username')
        if not re.match("^[A-Za-z0-9]+$", username):
            self.add_error('username', 'Only alphanumeric characters allowed in username.')
        return cleaned_data


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )