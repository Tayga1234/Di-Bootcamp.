from django.db import models

# Create your models here.
    
class Famille(models.Model):
    nom = models.CharField(max_length=50, null=True)
    
    
    def __str__(self):
        return self.nom
    

class Animal(models.Model):
    nom = models.CharField(max_length=50, null=True)
    pattes = models.IntegerField()
    poids = models.IntegerField()
    vitesse=models.IntegerField() 
    famille = models.ForeignKey(Famille, default=0, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nom

