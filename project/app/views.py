from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from utils.captcha import generate_captcha_text, generate_captcha_image

class LoginView(LoginView):
    template_name = 'login.html'
    # redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home') 
    
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['full_name']
        user.save()
        messages.success(self.request, "Account created successfully.")
        return super().form_valid(form)


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = 'login/'  
    
    
def captcha_image(request):
    text = generate_captcha_text()
    request.session['captcha_text'] = text  
    image_data = generate_captcha_image(text)
    return HttpResponse(image_data, content_type='image/png')
