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


def new_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Review created successfully")
    else:
        form = ReviewForm()
    return render(request, 'review/review_create.html', {'form': form})

class ReviewCreateView(CreateView):
    model = Review
    fields = ['ticket', 'rating', 'headline', 'body']
    template_name = 'review/review_create.html' 
    success_url = reverse_lazy('review:ticket_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Récupérer l'utilisateur connecté
        return super().form_valid(form)



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

    




