from django.urls import path
from . import views

urlpatterns = [
     path('',views.accueil, name='accueil'),
    path('location',views.locations, name='locations'),
    path('inscrire',views.inscrire, name='inscrire'),
    path('inscrire_client',views.ajoutercli, name='inscriree'),
    path('inscrire_vehicule',views.ajoutervehi, name='inscrirer'),
    path('location<int:id>/',views.afficher , name='afficher' ),
    path('client<int:id>/',views.modifier , name='modifier_cl' ),
    path('client',views.listclient , name='liste' ),
   
]