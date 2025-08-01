from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Booking,Itinerary
from .forms import BookingForm,ItineraryForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm


def home(request,):
    
    return render(request, 'Tour/home.html',)



def logoutUser(request):
    logout(request)
    return redirect('home')

