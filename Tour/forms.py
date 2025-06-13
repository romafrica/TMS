from django.forms import ModelForm
from .models import Booking, Itinerary

class BookingForm(ModelForm):
    class Meta:
        model=Booking
        fields='__all__'

class ItineraryForm(ModelForm):
    class Meta:
        model=Itinerary
        fields='__all__'