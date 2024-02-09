from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class UserRegistartionForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = {'username', 'email', 'first_name'}

    def check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['password2']

# Create a form for the GroceryItem model
class GroceryItemForm(forms.ModelForm):
    class Meta:
        model = GroceryItem
        fields = ['name', 'quantity', 'price', 'category', 'location', 'expiration_date', 'price_per_item']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_item': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Read-only
            'category': forms.Select(attrs={'class': 'form-select'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

# Create a form for the Category model
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


# Create a form for the Recipe model
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'