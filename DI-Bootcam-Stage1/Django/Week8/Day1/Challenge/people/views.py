from urllib import request
from django.shortcuts import render

import people

# Create your views here.
def index(request):
    people = [
    {
    'id': 1,
    'name': 'Bob Smith',
    'age': 35,
    'country': 'USA'
    },
    {
    'id': 2,
    'name': 'Martha Smith',
    'age': 60,
    'country': 'USA'
    },
    {
    'id': 3,
    'name': 'Fabio Alberto',
    'age': 18,
    'country': 'Italy'
    },
    {
    'id': 4,
    'name': 'Dietrich Stein',
    'age': 85,
    'country': 'Germany'
    },
    {
    'id': 5,
    'name': 'Sam Carter',
    'age': 20,
    'country': 'Canada'
    },
    {
    'id': 6,
    'name': 'Salim BG',
    'age': 27,
    'country': 'Dubai'
    },
    {
    'id': 7,
    'name': 'Feuble CFA',
    'age': 18,
    'country': 'Dorodougou'
    },
    {
    'id': 8,
    'name': 'Baba',
    'age': 12,
    'country': 'Espagne'
    }
    ]
    
    trie = sorted(people,key = lambda d: d['age'])

    
    
    context = {
        'people':trie,
        
    }

    return render(request,'people.html',context)



def detail(request,id):
   
    people = [
    {
    'id': 1,
    'name': 'Bob Smith',
    'age': 35,
    'country': 'USA'
    },
    {
    'id': 2,
    'name': 'Martha Smith',
    'age': 60,
    'country': 'USA'
    },
    {
    'id': 3,
    'name': 'Fabio Alberto',
    'age': 18,
    'country': 'Italy'
    },
    {
    'id': 4,
    'name': 'Dietrich Stein',
    'age': 85,
    'country': 'Germany'
    },
    {
    'id': 5,
    'name': 'Sam Carter',
    'age': 20,
    'country': 'Canada'
    },
    {
    'id': 6,
    'name': 'Salim BG',
    'age': 27,
    'country': 'Dubai'
    },
    {
    'id': 7,
    'name': 'Feuble CFA',
    'age': 18,
    'country': 'Dorodougou'
    },
    {
    'id': 8,
    'name': 'Baba',
    'age': 12,
    'country': 'Espagne'
    }
] 
    for key in people:
        for a,b in key.items():
            if a=='id' and b==id:
                pi=key
                
                
                context={
                    'people':pi
                }
                
                
                return render(request,'detail.html',context)