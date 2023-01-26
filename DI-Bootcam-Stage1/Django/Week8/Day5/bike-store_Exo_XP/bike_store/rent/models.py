from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=40)
    prenom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    ville =models.CharField(max_length=20)
    pays = models.CharField(max_length=20)
    
    
class Type_vehicule(models.Model):
    nom = models.CharField(max_length=30)

class Taille_vehicule(models.Model):
    nom = models.CharField(max_length=30)


class Vehicule(models.Model):
    date_creation = models.DateTimeField()
    cout = models.IntegerField()
    taille_id = models.ForeignKey(Taille_vehicule, default=0, on_delete=models.CASCADE)
    type_vehicule_id = models.ForeignKey(Type_vehicule, default=0, on_delete=models.CASCADE)
    
class Location(models.Model):
    date_location = models.DateTimeField()
    date_retour = models.DateTimeField()
    cout = models.IntegerField()
    client_id = models.ForeignKey(Client, default=0, on_delete=models.CASCADE)
    vehicule_id = models.ForeignKey(Vehicule, default=0, on_delete=models.CASCADE)
    
class Location_tarif(models.Model):
    tarif_jour = models.IntegerField()
    taille_id = models.ForeignKey(Taille_vehicule, default=0, on_delete=models.CASCADE)
    type_vehicule_id = models.ForeignKey(Type_vehicule, default=0, on_delete=models.CASCADE)