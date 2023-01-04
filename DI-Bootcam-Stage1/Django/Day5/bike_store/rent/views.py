from django.shortcuts import get_object_or_404, render
from .forms import RentalForm
# Create your views here.

from django.shortcuts import render
from .models import Customer, Rental

def rental_list(request):
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

