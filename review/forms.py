
from django import forms
from .models import Review, Ticket, UserFollows

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket 
        #fields = "__all__"
        fields = ['title', 'description', 'image']
        

# class ReviewForm(forms.ModelForm):
    
    
#     class Meta:
#         model = Review
#         fields = '__all__'
#         #fields = ['rating']
        #rating = forms.ChoiceField(widget=forms.RadioSelect, choices=RATING_CHOICES)
        

    # def __init__(self, *args, **kwargs):
    #     super(ReviewForm, self).__init__(*args, **kwargs)
    #     # Use a radio select widget instead of a dropdown for the score.
    #     self.fields["rating"] = forms.TypedChoiceField(
    #         choices=ReviewForm.RATING_CHOICES,
    #         coerce=int,
    #         empty_value=0,
    #         widget=forms.RadioSelect(),
    #     ) 
       


class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        #fields = ['followed_user', 'user']
        fields = '__all__'

# User unfollow form
class UserUnfollowForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user', 'user']
        #fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserUnfollowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-UserUnfollowForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'unfollow_user'

        self.helper.add_input(Submit('submit', 'Submit'))



# forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
class SubscribeForm(forms.Form):
    user_to_follow = forms.CharField(
        label="",
        #label="Suivre d'autres utilisateurs",
        widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}),
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


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import InlineRadios

class ReviewForm(forms.ModelForm):
    headline = forms.CharField(label="Title", max_length=128, widget=forms.TextInput())
    body = forms.CharField(label="Commentaire",max_length=8192, widget=forms.Textarea(),required=False)
    rating = forms.ChoiceField(initial=1, label="Rating",
                               # passer une classe dans l'attribut forms.RadioSelect(attrs=)  
                               widget=forms.RadioSelect(),
                            choices=((0, "- 0"), (1, "- 1"), (2, "- 2"), (3, "- 3"), (4, "- 4"), (5, '- 5')))

    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']

    

    # Crispy forms layout helper
    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('headline'),
        InlineRadios('rating', style="display: flex-inline; justify-content: space-around;"),
        Field('body', rows="10"),
        # Afficher l'image et pas le chemin vers l'image
        #Field('image', accept="image/*"),
        
    )

# Formulaire de suppression de ticket

class TicketDeleteForm(forms.ModelForm):
    class Meta:
        model = Ticket
        #fields = '__all__'
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(TicketDeleteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-TicketDeleteForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'ticket_delete'

        self.helper.add_input(Submit('submit', 'Submit'))