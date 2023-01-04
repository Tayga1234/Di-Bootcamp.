from django import forms
from .models import Gif, Category

from django import forms
from gifs.models import Gif, Category

class GifForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    
    class Meta:
        model = Gif
        fields = ['title', 'url', 'uploader_name', 'category']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
