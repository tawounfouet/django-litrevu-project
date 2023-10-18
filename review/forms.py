
from django import forms
from .models import Review, Ticket, UserFollows

class TicketForm(forms.ModelForm):

    # VALIDATIONS
    title = forms.CharField(label='Title',
                            min_length=3,
                            max_length=50,
                            widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(label='Description',
                                    min_length=10,
                                    max_length=1000,
                                    widget=forms.Textarea(attrs={'placeholder': 'Description', 'rows': 10}))
    image = forms.ImageField(label='Image',
                                widget=forms.FileInput(attrs={'placeholder': 'Image'}))
    user = forms.CharField(label='User',
                                widget=forms.TextInput(attrs={'placeholder': 'User'}))
    time_created = forms.DateField(label='Time Created',
                                widget=forms.TextInput(attrs={'placeholder': 'Time Created'}))
    
                                  


    class Meta:
        model = Ticket
        #fields = ['title', 'description', 'image', 'user', 'time_created']
        fields = '__all__'

        # Outside Widget
        widgets = {
            'phone': forms.TextInput(
                attrs={'style': 'font-size: 13px',
                       'placeholder': 'Phone',
                       'data-mask': '(+00) 00 00 00 00 00'
                       }
            )
        }


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