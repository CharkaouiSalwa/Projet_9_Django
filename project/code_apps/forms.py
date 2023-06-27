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
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']