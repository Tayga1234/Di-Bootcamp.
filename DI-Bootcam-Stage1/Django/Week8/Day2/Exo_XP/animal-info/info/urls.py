from django.urls import path #path function
from . import views # . is shorthand for the current directory

# one urlpattern per line
urlpatterns = [
    path('animaux/', views.animaux, name='animaux'),
    path('animal/<int:id>', views.animal, name='animal'),
    path('famille/<int:id>', views.family, name='family'),
]
