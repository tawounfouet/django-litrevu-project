
from django import forms
from .models import Review, Ticket, UserFollows

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket 
        fields = "__all__"


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


# forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
class SubscribeForm(forms.Form):
    user_to_follow = forms.CharField(
        label="Suivre d'autres utilisateurs",
        widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-SubscribeForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'subscribe'

        self.helper.add_input(Submit('submit', 'Submit'))


    # def __init__(self, *args, **kwargs):
    #     super(SubscribeForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_id = 'subscribe-form'
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Suivre'))