from django.conf import settings

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.utils import IntegrityError
from django.urls import reverse_lazy

from django.views.generic import View, FormView
from .forms import SignupForm, LoginForm

from .models import User
from review.models import UserFollows


class LoginPage(View):
    form_class = LoginForm
    template_name = "authentication/login.html"

    def get(self, request):
        form = self.form_class()
        message = ""
        context = {"form": form, "message": message}

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        message = ""
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                # message = f"Bonjour {user.username} ! Vous êtes connecté"
                return redirect(settings.LOGIN_REDIRECT_URL)
                # return redirect("authentication:user_profile", username=user.username)
            else:
                message = "Idendentifiants invalides"

        context = {"form": form, "message": message}

        return render(request, self.template_name, context)





## Une vue basé sur les fonction
# - Post : creer un abonnement
# - quand on est pas en post : créer des requetes pour avoir



def signup_page(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", context={"form": form})


def logout_user(request):
    logout(request)
    return redirect("login")
