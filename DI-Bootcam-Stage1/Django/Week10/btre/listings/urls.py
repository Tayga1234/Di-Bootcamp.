from django.urls import path
from . import views
# listings
urlpatterns = [
    path('listings', views.listings, name='listings'),
    path('<int:listing_id>', views.lisitng, name='listing'),
    path('search', views.search, name='search'),
]
