from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'), 
    path('clientList/',views.clientList,name='clientList'), 
    path('client/<int:pk>/',views.clientDetails,name='clientDetails'),       
    path('itinerary/',views.itinerary,name='itinerary'),
    path('newBooking/',views.newBooking,name='newBooking'),
    path('newItinerary/',views.newItinerary,name='newItinerary'),
    path('updateBooking/<str:pk>/',views.updateBooking,name='updateBooking'),
    path('updateItinerary/<str:pk>/',views.updateItinerary,name='updateItinerary'),
    path('deleteBooking/<str:pk>/',views.deleteBooking,name='deleteBooking'),
    path('deleteItinerary/<str:pk>/',views.deleteItinerary,name='deleteItinerary'),
    
    path('profile/',views.profile,name='update'),

]