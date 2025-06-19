from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]
