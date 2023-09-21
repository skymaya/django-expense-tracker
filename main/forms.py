import re
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import (
    User, 
    Expense, 
    ExpenseCategory, 
    SupportTicket,
    SupportTicketReply
)


class CustomModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Loop through the fields and set their labels to the verbose_name of the model field
        # keep the label setting / verbose_name in one place (model), be able to override fields
        # in form classes here and not need to set the label again
        for field_name, field in self.fields.items():
            model_field = self._meta.model._meta.get_field(field_name)
            if model_field.verbose_name:
                field.label = model_field.verbose_name


class TicketReplyForm(CustomModelForm):
    body = forms.CharField(widget=forms.Textarea())
    
    class Meta:
        model = SupportTicketReply
        fields = ['body']


class TicketForm(CustomModelForm):
    body = forms.CharField(widget=forms.Textarea())
    
    class Meta:
        model = SupportTicket
        fields = ['subject', 'body']


class ExpenseCategoryForm(CustomModelForm):
    hex_color = forms.CharField(
        max_length=7,
        help_text='For use with chart rendering',
        widget=forms.TextInput(attrs={'type': 'color'})
    )
    
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'long_description', 'slug', 'hex_color']


class ExpenseForm(CustomModelForm):
    
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