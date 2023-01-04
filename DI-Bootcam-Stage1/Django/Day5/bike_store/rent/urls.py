from django.urls import path
from . import views

urlpatterns = [
    path('rental/', views.rental_list, name='rental_list'),
    path('rental/<int:pk>', views.rental_detail, name='rental_detail'),
    path('rental/add', views.rental_add, name='rental_add'),
    path('customer/', views.customer_list, name='customer_list'),
]