from django.db import models

# Create your models here.
class Person(models.Model):
    nom = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, unique=True)
    phone_number= models.IntegerField()
    adresse=models.TextField(max_length=100, null=True) 
    
    def __str__(self):
        return self.nom
