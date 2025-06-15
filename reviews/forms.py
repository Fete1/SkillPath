# reviews/forms.py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5}),
        label="Rating (1-5)"
    )
    class Meta:
        model = Review
        fields = ['rating', 'comment']