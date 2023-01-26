
from rent.models import Client
from django import forms



class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'adresse', 'email', 'ville', 'pays']
        widgets = {
            'nom' :forms.TextInput(attrs = {'class': "form-control"}),
            'prenom' : forms.TextInput(attrs = {'class': "form-control"}),
            'adresse' :forms.TextInput(attrs = {'class': "form-control"}),
            'email' : forms.TextInput(attrs = {'class': "form-control"}),
            'ville' : forms.TextInput(attrs = {'class': "form-control"}),
            'pays' : forms.TextInput(attrs = {'class': "form-control"}),
        }
        
class EnregistreUser(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'adresse', 'email', 'ville', 'pays']
        widgets = {
            'nom' :forms.TextInput(attrs = {'class': "form-control"}),
            'prenom' : forms.TextInput(attrs = {'class': "form-control"}),
            'adresse' :forms.TextInput(attrs = {'class': "form-control"}),
            'email' : forms.TextInput(attrs = {'class': "form-control"}),
            'ville' : forms.TextInput(attrs = {'class': "form-control"}),
            'pays' : forms.TextInput(attrs = {'class': "form-control"}),
        }