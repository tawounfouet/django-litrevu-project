
from django import forms
from .models import Review, Ticket, UserFollows

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        #fields = ['title', 'description', 'image', 'user', 'time_created']
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        #fields = ['rating', 'headline', 'body', 'ticket', 'user', 'time_created']
        fields = '__all__'


class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        #fields = ['followed_user', 'user']
        fields = '__all__'