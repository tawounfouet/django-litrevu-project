
from django import forms
from .models import Review, Ticket, UserFollows

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket 
        fields = "__all__"
        



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body', 'ticket']
        #fields = '__all__'
        # utiliser un widget option button pour changer le rendu
        RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    #     rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        # Use a radio select widget instead of a dropdown for the score.
        self.fields["rating"] = forms.TypedChoiceField(
            choices=ReviewForm.RATING_CHOICES,
            coerce=int,
            empty_value=0,
            widget=forms.RadioSelect(),
        ) 
       


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