# malaria_app/forms.py

from django import forms
from .models import CatDogImage

class CatDogImageForm(forms.ModelForm):
    class Meta:
        model = CatDogImage
        fields = ['image']
        labels = {'image': 'Image à analyser'}