from http.client import HTTPResponse
from django.shortcuts import render

# Create your views here.

def index(request):

    animals = [
        {
            "id" :1,
            "name": "Dog",
            "legs": 4,
            "weight": 5.67,
            "height":4.2,
            "speed": 34,
            "family": 2
        },
        {
            "id": 2,
            "name": "Domestic Cat",
            "legs": 2,
            "weight": 5.67,
            "height":4.2,
            "speed": 34,
            "family": 1
        },
        {
            "id": 3,
            "name": "Panther",
            "legs": 2,
            "weight": 5.67,
            "height":4.2,
            "speed": 34,
            "family": 1 
        }
    ]
    

    families= [
        {
            "id": 1,
            "name": "Felidae"
        },
        {
            "id": 2,
            "name": "Caninae"
        },
        {
            "id": 3,
            "name": "mammal"
        },
        {
            "id": 4,
            "name": "reptile"
        },
        {
            "id": 5,
            "name": "insect"
        }
    ]
    
    context = {
        'animals':animals,
        'families':families,
        
    }

    return render(request,'posts/page.html',context)