from django.urls import path #path function
from . import views # . is shorthand for the current directory

# one urlpattern per line
urlpatterns = [
    path('persons/', views.personnes, name='personnes'),
    path('ajout/', views.create, name='create'),
    path('person_N/<str:nom>', views.person_N, name='person_N'),
    path('person_P/<int:phone_number>', views.person_P, name='person_P'),
]
