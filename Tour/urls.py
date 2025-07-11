from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name='home'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerUser,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'), 
    path('profile/<str:pk>/',views.userProfile,name='profile'),
    path('clientList/',views.clientList,name='clientList'), 
    path('client/<int:pk>/',views.clientDetails,name='clientDetails'),       
    path('itinerary/',views.itinerary,name='itinerary'),
    path('newBooking/',views.newBooking,name='newBooking'),
    path('newItinerary/',views.newItinerary,name='newItinerary'),
    path('updateBooking/<str:pk>/',views.updateBooking,name='updateBooking'),
    path('updateItinerary/<str:pk>/',views.updateItinerary,name='updateItinerary'),
    path('deleteBooking/<str:pk>/',views.deleteBooking,name='deleteBooking'),
    path('deleteItinerary/<str:pk>/',views.deleteItinerary,name='deleteItinerary'),
    

]