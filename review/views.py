from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views import generic



# Create your views here.
def home(request):
    return HttpResponse("Hello, You're at the review home page.")
    #return render(request, 'index.html')

def about(request):
    return HttpResponse("About Us")
    #return render(request, 'about.html')

def contact(request):
    return HttpResponse("Contact Us")
