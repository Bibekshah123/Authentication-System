from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('captcha_image/', captcha_image, name='captcha_image'),
    # path('activate/<uidb64>/<token>/', activate_account, name='activate'),



]
