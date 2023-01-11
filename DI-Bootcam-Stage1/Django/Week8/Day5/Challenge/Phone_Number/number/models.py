from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Person(models.Model):
    nom = models.CharField(max_length=50, null=True)   
    phone_number= PhoneNumberField()
    
    def __str__(self):
        return self.nom
