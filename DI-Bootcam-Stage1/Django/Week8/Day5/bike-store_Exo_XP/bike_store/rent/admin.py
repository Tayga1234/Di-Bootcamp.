from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Client)
admin.site.register(Vehicule)
admin.site.register(Taille_vehicule)
admin.site.register(Type_vehicule)
admin.site.register(Location)
admin.site.register(Location_tarif)