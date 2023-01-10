from todo.models import Todo
from django import forms



class TodoForm(forms.ModelForm):
    class Meta:
        model= Todo
        fields=['titre','detail','categorie_id','date_creation', 'date_echeance']
        widgets = {
            'date_creation' :forms.DateTimeInput(attrs = {'type': "date"}),
            'date_echeance' :forms.DateTimeInput(attrs = {'type': "date"}),
        }