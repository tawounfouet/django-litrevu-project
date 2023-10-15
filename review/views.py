from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from authentication import models
from .models import Review, Ticket, UserFollows
from .forms import TicketForm, ReviewForm, UserFollowsForm


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


def new_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Ticket created successfully")
    else:
        form = TicketForm()
    return render(request, 'review/ticket_create.html', {'form': form})


# all tickets view
class TicketListView(generic.ListView):
    model = Ticket
    template_name = 'review/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 5
    queryset = Ticket.objects.all().order_by('-time_created')

# ticket detail view
class TicketDetailView(generic.DetailView):
    model = Ticket
    template_name = 'review/ticket_detail.html'
    context_object_name = 'ticket'


def new_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Review created successfully")
    else:
        form = ReviewForm()
    return render(request, 'review/review_create.html', {'form': form})

