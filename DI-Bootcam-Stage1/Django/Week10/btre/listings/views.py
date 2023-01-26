from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render

from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



# Create your views here.


def listings(request):
    listings = Listing.objects.all()

    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)


def lisitng(request, listing_id):
    listing=get_object_or_404(Listing, pk=listing_id)

    context={
        'listing':listing,
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    list= Listing.objects.order_by('-list_data').filter(is_published=True)[:3]
    if request.method=='GET':
        city=request.GET.get('city')
        if city is not None:
            list = Listing.objects.filter(city__icontains=city)
                  
            state=request.GET.get('state')
            if state is not None:
                bedrooms=request.GET.get('bedrooms')
                if bedrooms is not None:
                    price=request.GET.get('price')
                    if price is not None:
                        list = Listing.objects.filter(state__icontains=state,bedrooms__lte=bedrooms, price__lte=price)
                
            
    else:
        list= Listing.objects.order_by('-list_data').filter(is_published=True)[:3]       
    
    context = {
       
        'home':list
    }

    return render(request, 'listings/search.html', context)

