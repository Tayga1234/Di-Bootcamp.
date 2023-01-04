from django.shortcuts import render

from info.models import Person

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