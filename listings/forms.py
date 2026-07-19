from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        # Fields available for the landlord to fill out
        fields = ['title', 'description', 'location', 'price', 'rooms', 'housing_type']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'location': 'Location',
            'price': 'Price',
            'rooms': 'Number of rooms',
            'housing_type': 'Housing type',
        }