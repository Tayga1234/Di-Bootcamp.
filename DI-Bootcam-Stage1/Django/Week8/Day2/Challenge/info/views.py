
from pyexpat.errors import messages
from django.shortcuts import render, redirect

from info.models import Person
from info.forms import PersonForm


def create(request):
    if request.method=='POST':
        #form= PersonForm(request.POST).save()
        nm = request.POST['nom']
        em= request.POST['email']
        ph = request.POST['phone_number']
        adr= request.POST['adresse']
        
        ma_personne = Person( nom=nm, email=em , phone_number=ph , adresse=adr)
        ma_personne.save()
        messages.success(request, 'enregistré avec succès')
        return redirect('/create')
    
    return render (request,'create.html')

# Create your views here.
def personnes (request):
    personnes=Person.objects.all()
    context={
        'personnes':personnes,
        
    }
    return render (request,'personnes.html', context)

#cette vue recupere le nom et affiche les infos de la personne
def person_N (request,nom):
    detail=Person.objects.get(nom=nom)
 
    context={
        'detail': detail
    }
    return render (request,'person.html', context)

#cette vue recupere le numero et affiche les infos de la personne

def person_P (request, phone_number):
    detail = Person.objects.get(phone_number=phone_number)
    context={
        'detail': detail
    }
    return render (request,'person.html', context)