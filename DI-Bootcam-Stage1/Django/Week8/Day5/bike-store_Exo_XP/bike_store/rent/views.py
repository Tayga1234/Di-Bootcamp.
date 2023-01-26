from django.shortcuts import get_object_or_404, render,redirect
from .form import ClientForm, EnregistreUser
# Create your views here.
from .models import *
from django.shortcuts import render
from django.contrib import messages

''' def rental_list(request):
    rentals = Rental.objects.order_by('return_date', 'rental_date')
    return render(request, 'rent/rental_list.html', {'rentals': rentals})

def rental_detail(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    return render(request, 'rent/rental_detail.html', {'rental': rental})

def rental_add(request):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            # Save the rental to the database
            pass
    else:
        form = RentalForm()
    return render(request, 'rent/rental_add.html', {'form': form})

def customer_list(request):
    customers = Customer.objects.order_by('last_name', 'first_name')
    return render(request, 'rent/customer_list.html', {'customers': customers})
 '''

def accueil(request):
    vehicule = Vehicule.objects.all()
    
    
    return render(request,'index.html', {'voiture' : vehicule})

def locations(request):
    locations = Location.objects.all()
    
    return render(request,'listlocation.html', {'location' : locations})

def listclient(request):
    clien = Client.objects.all()
    
    return render(request,'listclient.html', {'clients' : clien})

def afficher(request, id):
    if request.method == 'POST':
        detail = Location.objects.get(pk=id)
      
    else:
        detail = Location.objects.get(pk=id)
   
    return render(request, 'locdetail.html', {'info':detail})



def inscrire(request):  
    clien = Client.objects.all()
    vhi = Vehicule.objects.all()
    if request.method == 'POST':
        clie = request.POST['client']
        vehicul = request.POST['voiture']
        date_crea = request.POST['date_crea']
        date_ret= request.POST['date_ret']
        cout = request.POST['cout'] 
        mon_user = Location( client_id_id=clie, vehicule_id_id=vehicul, date_location=date_crea, date_retour=date_ret, cout=cout)
        mon_user.save()
        messages.success(request, 'votre compte a été crée')
        return redirect('accueil')
   
    return render(request, 'ajouterloc.html',{'inf':clien, 'voit':vhi} )

def ajoutervehi(request): 
    clien = Taille_vehicule.objects.all()
    vhi = Type_vehicule.objects.all() 
    if request.method == 'POST':
        clie = request.POST['taille']
        vehicul = request.POST['type']
        date_crea = request.POST['date_crea']
        cout = request.POST['cout'] 
        mon_vehi = Vehicule( taille_id_id=clie, type_vehicule_id_id=vehicul, date_creation=date_crea, cout=cout)
        mon_vehi.save()
        messages.success(request, 'Enregistrement validé')
        return redirect('accueil')
   
    return render(request, 'ajoutervhi.html',{'inf':clien, 'voit':vhi}  )


def ajoutercli(request):  
    ''' if request.method == 'POST':
        nm = request.POST['nom']
        pnm = request.POST['prenom']
        adr = request.POST['adresse']
        em= request.POST['email']
        vil = request.POST['ville'] 
        pay = request.POST['pays'] 
        mon_client = Client( nom=nm, prenom=pnm, adresse=adr, email=em, ville=vil, pays=pay) '''
    form=ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'client enregistré avec succès')
        return redirect('accueil')
    context={
        'form':form
    }
   
    return render(request, 'ajoutercli.html', context )

def modifier(request, id):
    if request.method == 'POST':
        pi = Client.objects.get(pk=id)
        fm = EnregistreUser(request.POST, instance=pi )
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Information du client modifié avec succès')
            return redirect('accueil')
    else:
        pi = Client.objects.get(pk=id)
        fm = EnregistreUser(instance= pi)
    return render(request, 'modifier_client.html', {'form':fm})


   