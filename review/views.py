from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.views.generic.edit import CreateView
from authentication import models
from authentication.models import User
from .models import Review, Ticket, UserFollows
from .forms import TicketForm, TicketDeleteForm, ReviewForm, SubscribeForm, UnSubscribeForm
from django.views.generic import DeleteView

from django.db.models import Count, Value, CharField, OuterRef, Subquery

from itertools import chain
from django.db.models import CharField, Value, Q
from django.shortcuts import render




def get_users_viewable_reviews(request):
    """Return a queryset of reviews that the user can view."""
    users_followed = UserFollows.objects.filter(user_id=request.user.id).values(
        "followed_user_id"
    )
    
    # Liste des utilisateurs suivis par l'utilisateur connecté
    list_id = [id["followed_user_id"] for id in users_followed]
    
    # Filtrer les critiques des utilisateurs suivis
    reviews_users_followed = Review.objects.filter(user__in=list_id)
    
    # Union des critiques des utilisateurs suivis et des critiques liées aux tickets de l'utilisateur
    reviews_users_followed = reviews_users_followed | Review.objects.filter(ticket__user_id=request.user.id)

    return reviews_users_followed


def get_users_viewable_tickets(request):
    """Return a queryset of a tickets that the user can view"""
    users_followed = UserFollows.objects.filter(user_id=request.user.id).values(
        "followed_user_id"
    )
    list_id = [id["followed_user_id"] for id in users_followed]
    list_id.append(request.user.id)
    users_objects = User.objects.filter(id__in=list_id)
    tickets_users_followed = Ticket.objects.filter(user__in=users_objects)
    return tickets_users_followed



@login_required
def feed(request):
    # Récupérez les critiques visibles par l'utilisateur
    reviews = get_users_viewable_reviews(request)

    # Comptez le nombre de critiques par ticket
    ticket_reviews_count = Review.objects.filter(ticket_id=OuterRef('pk')).values('ticket_id').annotate(
        num_reviews=Count('id')
    ).values('num_reviews')

    # Récupérez les tickets visibles par l'utilisateur avec le nombre de critiques associées
    tickets = get_users_viewable_tickets(request).annotate(
        num_reviews=Subquery(ticket_reviews_count, output_field=CharField())
    )

    # Ajoutez une annotation pour différencier les critiques et les tickets
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()), 
                               review_number=Count('review'))

    # Combiner et trier les deux types de publications
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


class TicketListView(generic.ListView):
    model = Ticket
    template_name = 'review/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 5
    queryset = Ticket.objects.all().order_by('-time_created')
   # modifier la queryset pour afficher ticket et review

# ticket detail view
class TicketDetailView(generic.DetailView):
    model = Ticket
    template_name = 'review/ticket_detail.html'
    context_object_name = 'ticket'


def delete_ticket(request, ticket_id):
    """Supprimer un ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Vérifier si l'utilisateur connecté est l'auteur du ticket
    if request.user != ticket.user:
        # Si non, rediriger l'utilisateur vers la liste des tickets (ou autre page appropriée)
        return HttpResponseRedirect(reverse('review:ticket_list'))

    if request.method == 'POST':
        form = TicketDeleteForm(request.POST, instance=ticket)
        if form.is_valid():
            # Faire pareil pour la suppression // vérification
            ticket.delete()
            return redirect('review:ticket_list')
    else:
        form = TicketDeleteForm(instance=ticket)

    return render(request, 'review/ticket_delete.html', {'form': form, 'ticket': ticket})


class TicketUpdateView(generic.UpdateView):
    model = Ticket
    template_name = 'review/ticket_update.html'
    fields = ['title', 'description', 'image']
    success_url = reverse_lazy('review:ticket_list')

    def dispatch(self, request, *args, **kwargs):
        ticket = self.get_object()
        
        # Vérifier si l'utilisateur connecté est l'auteur du ticket
        if request.user != ticket.user:
            # Si non, rediriger l'utilisateur vers la liste des tickets (ou autre page appropriée)
            return HttpResponseRedirect(reverse('review:ticket_list'))
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user  # Récupérer l'utilisateur connecté
        # Faire pareil pour la suppression
        return super().form_valid(form)



class TicketReviewListView(LoginRequiredMixin, generic.ListView):
    template_name = 'review/ticket_review_list.html'
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        # Récupérez l'utilisateur connecté
        user = self.request.user

        # Récupérez les tickets et reviews de l'utilisateur connecté
        tickets = Ticket.objects.filter(user=user).order_by('-time_created')
        reviews = Review.objects.filter(user=user).order_by('-time_created')

        # Combinez les listes de tickets et de reviews
        items = list(tickets) + list(reviews)

        # Triez la liste combinée par time_created
        items.sort(key=lambda x: x.time_created, reverse=True)

        return items


@login_required 
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


            #return HttpResponse("Ticket and Review created successfully")
            return redirect('review:ticket_detail', ticket_id=ticket.id)
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, 'review/review_create_blank.html', {'ticket_form': ticket_form, 'review_form': review_form})


@login_required
def new_review(request, ticket_id):
    """Create a new review."""
    ticket_instance = Ticket.objects.get(id=ticket_id)
    user = request.user
    if request.method == "POST":
        form_review = ReviewForm(request.POST)
        if form_review.is_valid():
            form_review.cleaned_data
            review_instance = Review(
                ticket=ticket_instance,
                rating=form_review.cleaned_data["rating"],
                headline=form_review.cleaned_data["headline"],
                body=form_review.cleaned_data["body"],
                user=user,
            )
            review_instance.save()
            ticket_instance.has_review = True
            ticket_instance.save()
            return redirect("review:feed")
    else:
        ticket_instance = Ticket.objects.get(id=ticket_id)
        review_form = ReviewForm()
        review_form.ticket = ticket_instance
        return render(
            request,
            'review/review_create.html',
            {"ticket_instance": ticket_instance, "review_form": review_form},
        )

class ReviewListView(generic.ListView):
    model = Review
    template_name = 'review/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 5
    queryset = Review.objects.all().order_by('-time_created')


class ReviewDetailView(generic.DetailView):
    model = Review
    template_name = 'review/review_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.object

        return context


@login_required
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


@login_required
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
    return render(request, 'review/subscriptions.html', context)



@login_required
def unfollow_user(request):
    if request.method == 'POST':
        form = UnSubscribeForm(request.POST)
        if form.is_valid():
            user_to_unfollow = form.cleaned_data['user_to_unfollow']
            UserFollows.objects.filter(
                user=request.user,
                followed_user=user_to_unfollow
            ).delete()
            messages.success(request, f'Vous vous êtes désabonné de {user_to_unfollow.username}.')
            return redirect("review:subscriptions")  # Redirigez vers la page d'accueil ou une autre vue.
    else:
        form = UnSubscribeForm()

    return render(request, 'review/unfollow_user.html', {'form': form})
