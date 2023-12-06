from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import LoginForm, SignupForm


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
