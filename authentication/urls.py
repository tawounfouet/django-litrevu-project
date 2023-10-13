
from django.urls import path

from authentication import views

from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)


app_name = 'authentication'
urlpatterns = [ 
    path('login/', views.LoginPage.as_view(), name='login'),
    #path('login/', views.login_page, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_page, name='signup'),
    
]

