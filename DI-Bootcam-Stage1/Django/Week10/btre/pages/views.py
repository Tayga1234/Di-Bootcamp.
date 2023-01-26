from django.shortcuts import render
from listings.models import Listing
from realtors.models import Realtor 



# Create your views here.
def index(request, *args, **kwargs):
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
                        list = Listing.objects.filter(state__icontains=state, bedrooms__lte=bedrooms, price__lte=price)
                
            
    else:
        list= Listing.objects.order_by('-list_data').filter(is_published=True)[:3]
    
    context = {
       
        'home':list
    }

    return render(request,'pages/index.html', context)

    
    
'''  
    lalist= Listing.objects.order_by('-list_data').filter(is_published=True)[:3]
    list=Listing.objects.all()
    
    if request.method=='POST':
        list = Listing.objects.order_by('-list_data').filter(city=request.POST['city']).values()
        lalist=list
        
    else:
        lalist= Listing.objects.order_by('-list_data').filter(is_published=True)[:3]
    '''
    
       

def about(request):
    realtors=Realtor.objects.order_by('-hire_date')

    mvp_realtors=Realtor.objects.all().filter(is_mvp=True)

    context= {
        'realtors':realtors,
        'mvp_realtors':mvp_realtors
    }


    return render(request, 'pages/about.html', context)
