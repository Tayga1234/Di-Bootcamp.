from django.db import models

# Create your models here.

class Categorie(models.Model):
    nom = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images', blank=True)
    
    def __str__(self):
        return self.nom    

class Todo(models.Model):
    titre = models.CharField(max_length=20)
    detail = models.TextField(max_length=50)
    has_been_done=models.BooleanField(default=False)
    date_creation = models.DateTimeField()
    date_completion = models.DateTimeField(null=True)
    date_echeance = models.DateTimeField()
    categorie_id = models.ForeignKey(Categorie, default=0, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom  
    