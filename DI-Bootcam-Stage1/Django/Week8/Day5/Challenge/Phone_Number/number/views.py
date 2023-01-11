from django.shortcuts import render

# Create your views here.

from pyexpat.errors import messages
from django.shortcuts import render, redirect


from number.models import Person
from .forms import Person,PersonForm


def create(request):
    form=PersonForm(request.POST)
    if form.is_valid():
        form.save()
        
        return redirect('/persons')
    context= {
        'form':form
    }
    
    return render (request,'create.html',context)

# Create your views here.
def personnes (request):
    personnes=Person.objects.all()
    context={
        'personnes':personnes,
        
    }
    return render (request,'personnes.html', context)

