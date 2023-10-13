from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from authentication import models


# Create your views here.
def home(request):
    # recupérer le user connecté dans une variable
    user = request.user 
   
    #return HttpResponse("Hello {user.username}, Welcome to LITRevu !".format(user=user))
    return render(request, 'review/index.html')

def about(request):
    #return HttpResponse("About Us")
    return render(request, 'review/about.html')

def contact(request):
    #return HttpResponse("Contact Us")
    return render(request, 'review/contact.html')
