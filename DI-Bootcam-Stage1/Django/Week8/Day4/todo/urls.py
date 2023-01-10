from django.urls import path,include
from .import views

urlpatterns = [

    path('creation/',views.creation, name='creation'),
    path('',views.list, name='list'),
]