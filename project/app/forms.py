from django import forms
from django.contrib.auth.models import User
import re

class RegisterForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Susant Bist',
        })
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com',
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password',
            'title': 'Minimum 8 characters, including uppercase, lowercase, digit and symbol',
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat your password',
        }),
        label='Confirm Password'
    )
    captcha_input = forms.CharField(
        label="Enter the CAPTCHA",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type the characters shown in the image',
        })
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'password']  # Note: 'full_name' & 'email' are custom

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get("password")
    confirm_password = cleaned_data.get("confirm_password")
    user_input = cleaned_data.get("captcha_input", "").upper()
    actual_captcha = self.request.session.get('captcha_text', '').upper()

    if not password or not confirm_password:
        raise forms.ValidationError("Password and confirm password are required.")

    if password != confirm_password:
        raise forms.ValidationError("Passwords do not match.")

    if not self.password_strength(password):
        raise forms.ValidationError("Password is too weak.")

    if user_input != actual_captcha:
        raise forms.ValidationError("Incorrect CAPTCHA entered.")

    return cleaned_data

def password_strength(self, password):
    import re
    if not password:
        return False
    return all([
        len(password) >= 8,
        re.search(r'[A-Z]', password),
        re.search(r'[a-z]', password),
        re.search(r'[0-9]', password),
        re.search(r'[\W_]', password),
    ])

