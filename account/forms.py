from django_countries.fields import CountryField

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterUserForm(UserCreationForm):
    """
    Form for registering a new user
    """
    username = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )

    def is_password_match(password1, password2):
        """
        Method asserts if password1 and password2 are equal
        returns True/False
        """
        if password1 == password2:
            return True
        else:
            return False


class UserProfileForm(forms.ModelForm):
    """
    Form for creating user information
    """
    bio = forms.Textarea()
    age = forms.IntegerField(required=False)
    gender = forms.CharField(max_length=150, required=False)
    location = forms.CharField(max_length=150, required=False)
    profile_img = forms.ImageField(required=False)
    countries_visited = CountryField()
    
    class Meta:
        model = UserProfile
        fields = [
            'bio',
            'age',
            'gender',
            'location',
            'profile_img',
            'countries_visited'
        ]
        