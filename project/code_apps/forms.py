from django import forms
from .models import Ticket, Review

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
        }

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(str(i), str(i)) for i in range(6)]

    title = forms.CharField()
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))


    class Meta:
        model = Review
        fields = ('title', 'rating', 'comment' )
