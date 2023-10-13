from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from django.views.generic import View

from authentication import forms


class LoginPage(View):
    form_class = forms.LoginForm
    template_name = 'authentication/login.html'

    def get(self, request):
        form = self.form_class()
        message = ''
        context = {
            "form": form,
            "message": message}

        return render(request, self.template_name,  context)

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                #message = f"Bonjour {user.username} ! Vous êtes connecté"
                return redirect('review:home')
            else:
                message = 'Idendentifiants invalides'

        context = {
            "form": form,
            "message": message}

        return render(request, self.template_name, context)



def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})





def logout_user(request):
    logout(request)
    return redirect('login')




