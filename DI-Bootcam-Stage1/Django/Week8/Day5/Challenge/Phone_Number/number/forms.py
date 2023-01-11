from django.forms import ModelForm
from django import forms
from number.models import Person
from phonenumber_field.modelfields import PhoneNumberField


class PersonForm(forms.ModelForm):
    phone_number=PhoneNumberField()
    
    class Meta:
        model=Person
        fields=['nom','phone_number']
        widgets = {
            'nom' :forms.TextInput(attrs = {'class': "form-control"}),
            
        }