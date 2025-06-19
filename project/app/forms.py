import requests
from django.conf import settings
from django import forms
from django.contrib.auth.models import User
import re

class RegisterForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, label="Full Name")
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        # Password check
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        if not self.password_strength(password):
            raise forms.ValidationError("Password is too weak.")

        # reCAPTCHA validation
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            raise forms.ValidationError("Invalid reCAPTCHA. Please try again.")

        return cleaned_data

    def password_strength(self, password):
        return all([
            len(password) >= 8,
            re.search(r'[A-Z]', password),
            re.search(r'[a-z]', password),
            re.search(r'[0-9]', password),
            re.search(r'[\W_]', password),
        ])
