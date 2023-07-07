from django import forms
from litreview.models import Ticket, Review

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
        }



class ReviewForm(forms.ModelForm):
    headline = forms.CharField(label='titre', max_length=128)
    RATING_CHOICES = [(str(i), str(i)) for i in range(6)]
    rating = forms.ChoiceField(label='note', choices=RATING_CHOICES, widget=forms.RadioSelect)
    body = forms.CharField(label='Commentaire',widget=forms.Textarea(attrs={'rows': 4}))


    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
