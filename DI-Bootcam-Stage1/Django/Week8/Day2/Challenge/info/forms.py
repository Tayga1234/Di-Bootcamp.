from django.forms import ModelForm
from django import forms
from info.models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model=Person
        fields=['nom','email','phone_number', 'adresse']
        widgets = {
            'nom' :forms.TextInput(attrs = {'class': "form-control"}),
            'email' : forms.TextInput(attrs = {'class': "form-control"}),
            'phone_number' : forms.NumberInput(attrs = {'class': "form-control"}),
            'adresse' :forms.TextInput(attrs = {'class': "form-control"}),
            
        }