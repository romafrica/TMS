from django.forms import ModelForm
from .models import 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Destination, DestinationImage, Room, Restaurant, Activity, Information, DateRange,Booking, Itinerary, TravelLeg
from django import forms
from .models import Activity

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        



class BookingForm(ModelForm):
    class Meta:
        model=Booking
        fields='__all__'

class ItineraryForm(ModelForm):
    class Meta:
        model=Itinerary
        fields='__all__'