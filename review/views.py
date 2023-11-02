from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from django.views.generic.edit import CreateView
from authentication import models
from authentication.models import User
from .models import Review, Ticket, UserFollows
from .forms import TicketForm, ReviewForm, SubscribeForm


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


# def new_ticket(request):
#     if request.method == 'POST':
#         form = TicketForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("Ticket created successfully")
#     else:
#         form = TicketForm()
#     return render(request, 'review/ticket_create.html', {'form': form})

from itertools import chain
from django.db.models import CharField, Value
from django.shortcuts import render

@login_required
def get_users_viewable_reviews(user):
    """Renvoie un ensemble de requêtes des billets et avis de tous les utilisateurs suivis par l'utilisateur connecté."""
    # Obtenir tous les utilisateurs suivis par l'utilisateur connecté.
    followed_users = UserFollows.objects.filter(user=user)
    # Obtenir tous les billets et avis des utilisateurs suivis.
    reviews = Review.objects.filter(user__in=followed_users)
    
    return reviews

@login_required
def get_users_viewable_tickets(user):
    """Renvoie un ensemble de requêtes des billets et avis de l'utilisateur connecté."""
    # Obtenir tous les billets et avis de l'utilisateur connecté.
    tickets = Ticket.objects.filter(user=user)

    return tickets


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # combine and sort the two types of posts
    posts = sorted(chain(reviews, tickets),
                   key=lambda post: post.time_created,
                   reverse=True)
    
    return render(request, 'review/feed.html', context={'posts': posts})







class TicketCreateView(CreateView):
    model = Ticket
    fields = ['title', 'description', 'image']
    template_name = 'review/ticket_create.html'  # Remplacez par le nom de votre template
    success_url = reverse_lazy('review:ticket_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Récupérer l'utilisateur connecté
        return super().form_valid(form)



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

# Supprimer un ticket
class TicketDeleteView(generic.DeleteView):
    model = Ticket
    template_name = 'review/ticket_delete.html'
    success_url = reverse_lazy('review:ticket_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# utiliser un formulaire en post pour la delete view


 # ticket edit view
class TicketUpdateView(generic.UpdateView):
    model = Ticket
    template_name = 'review/ticket_update.html'
    fields = ['title', 'description', 'image']
    success_url = reverse_lazy('review:ticket_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Récupérer l'utilisateur connecté
        return super().form_valid(form)



# 
def new_review_blank(request):
    """ creer une critique avec deux formulaires : le formulaire de ticket et le formulaire de review en utilisant une view basée sur une fonction"""
    user = request.user

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST, request.FILES)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = user
            review.ticket = ticket
            review.save()


            return HttpResponse("Ticket and Review created successfully")
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, 'review/review_create.html', {'ticket_form': ticket_form, 'review_form': review_form})




# A faire 
# def new_review(request):


# Liste des reviews
class ReviewListView(generic.ListView):
    model = Review
    template_name = 'review/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 5
    queryset = Review.objects.all().order_by('-time_created')

# url for review list
# path('reviews', views.ReviewListView.as_view(), name='review_list'),
# url for review in template
# {% url 'review:review_list' %}

class ReviewDetailView(generic.DetailView):
    model = Review
    template_name = 'review/review_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.object

        return context


# def new_review_blank(request):
#     if request.method == 'POST':
#         form = ReviewForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("Review created successfully")
#     else:
#         form = ReviewForm()
#     return render(request, 'review/review_create.html', {'form': form})


# Use ReviewForm to create and fonction based view to create a review
def new_review(request, ticket_id):
    # Récupérer le ticket dont l'ID est ticket_id
    ticket = get_object_or_404(Ticket, id=ticket_id)

    #return HttpResponse(f"Ticket: {ticket.title} | {ticket.description} | {ticket.image}")


    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Créer un objet Review à partir du formulaire mais ne pas le sauvegarder tout de suite
            review = form.save(commit=False)
            # Récupérer l'utilisateur connecté et l'associer à la review
            review.user = request.user
            # Récupérer le ticket et l'associer à la review
            review.ticket = ticket
            # Sauvegarder la review
            review.save()
            return redirect('review:ticket_detail', ticket_id=ticket_id)
    else:
        form = ReviewForm()
    return render(request, 'review/review_create.html', {'form': form, 'ticket': ticket})






def user_profile(request, username):
    # Récupérer l'utilisateur dont le profil est affiché
    profile_user = get_object_or_404(User, username=username)

    # Récupérer l'utilisateur connecté (si authentifié)
    current_user = request.user if request.user.is_authenticated else None

    context = {
        'profile_user': profile_user,
        'current_user': current_user,
    }

    return render(request, 'review/user_profile.html', context)


def follow_user(request):
    # Récupérer la liste des utilisateurs que vous suivez (following)
    user_following = UserFollows.objects.filter(user=request.user)

    # Récupérer la liste des utilisateurs qui vous suivent (followers)
    user_followers = UserFollows.objects.filter(followed_user=request.user)

    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            username_to_follow = form.cleaned_data['user_to_follow']

            # Vérifier si l'utilisateur essaie de se suivre lui-même
            if username_to_follow == request.user.username:
                messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
            else:
                try:
                    # Vérifier si l'utilisateur cible existe
                    user_to_follow = User.objects.get(username=username_to_follow)
                    is_following = UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists()

                    if is_following:
                        messages.error(request, f"Vous suivez déjà {username_to_follow} !")
                    else:
                        # Créer une nouvelle relation de suivi
                        follow = UserFollows(user=request.user, followed_user=user_to_follow)
                        follow.save()
                        messages.success(request, f"Vous suivez maintenant {username_to_follow} !")
                except User.DoesNotExist:
                    messages.error(request, f"Utilisateur {username_to_follow} n'existe pas.")

    else:
        form = SubscribeForm()

    context = {
        'form': form,
        'user_following': user_following,
        'user_followers': user_followers,
    }
    return render(request, 'review/follow_user.html', context)


# Faire un un formulaire plutot : ne jamais faire en get les choses qui vont modifier la BD
# C'est bien de demander une confirmation avant la suppression 
# classe de suppression DeleteView --> Voir doc
# ou bien utiliser une petite boite de dialogue en JS pour confirmer la suppremier
# vérifier également dans la suppression que l'on soit l'auteur de l'abonnement
#@login_required
def unfollow_user(request, user_id):
    # Récupérer l'utilisateur que vous souhaitez ne plus suivre
    user_to_unfollow = get_object_or_404(User, id=user_id)

    # Vérifier si vous suivez déjà cet utilisateur
    try:
        follow = UserFollows.objects.get(user=request.user, followed_user=user_to_unfollow)
        follow.delete()
        messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username} !")
    except UserFollows.DoesNotExist:
        messages.error(request, f"Vous ne suiviez pas {user_to_unfollow.username}.")

    # rester sur la meme page
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    




