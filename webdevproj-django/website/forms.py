from django import forms
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'cooking_time', 'difficulty', 'instructions']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')