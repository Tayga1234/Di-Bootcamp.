from django.shortcuts import render

from todo.models import Todo
from .forms import TodoForm,Todo
# Create your views here.


def creation(request):
    form=TodoForm(request.POST or None)
    if form.is_valid():
        form.save()
    context={
        'form':form
    }
    return render(request,'creation.html',context)

def list (request):
    taches=Todo.objects.all()
    context={
        'taches':taches,
        
    }
    return render (request,'list.html', context)
