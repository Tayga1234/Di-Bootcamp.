from django.urls import path #path function
from . import views # . is shorthand for the current directory

# one urlpattern per line
urlpatterns = [
    path('persons/', views.personnes, name='personnes'),
    path('ajout/', views.create, name='create'),
 ]
