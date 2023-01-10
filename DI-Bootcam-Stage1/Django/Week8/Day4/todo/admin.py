from django.contrib import admin

from todo.models import Categorie,Todo

# Register your models here.
admin.site.register(Todo)
admin.site.register(Categorie)