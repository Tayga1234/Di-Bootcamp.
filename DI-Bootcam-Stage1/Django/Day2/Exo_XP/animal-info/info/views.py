from django.shortcuts import render

from info.models import Animal, Famille

# Create your views here.

def animaux (request):
    animaux=Animal.objects.all()
    familles=Famille.objects.all()
    context={
        'animaux':animaux,
        'familles':familles
    }
    return render (request,'animaux.html', context)




def animal (request, id):
    detail=Animal.objects.get(pk=id)
 
    context={
        'detail': detail
    }
    return render (request,'animal.html', context)




def family (request, id):
    
    family=Animal.objects.all().filter(famille_id=id)
    nom_F=Famille.objects.all()     
    context={
        'family': family,
        'nom_F':nom_F
    }
    return render (request,'family.html', context)




