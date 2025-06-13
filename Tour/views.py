from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Booking,Itinerary
from .forms import BookingForm,ItineraryForm






def home(request,):
    
    return render(request, 'Tour/home.html',)

def dashboard(request):
    bookings=Booking.objects.all()
    itinerary= Itinerary.objects.all()
    context={'bookings':bookings, 'itinerary':itinerary}
    return render(request,'Tour/dashboard.html',context)

def clientList(request):
    bookings=Booking.objects.all()
    context={'bookings':bookings}
    return render(request,'Tour/client_list.html',context)



def clientDetails(request,pk):
    bookings=Booking.objects.get(id=pk)
    context={"bookings":bookings}
    return render(request,'Tour/client_details.html', context)

def itinerary(request):
    itinerary= Itinerary.objects.all()
    context={'itinerary':itinerary}
    return render(request, 'Tour/itinerary.html',context)

def newBooking(request):
    form=BookingForm()
    if request.method=="POST":
        form=BookingForm(request.POST)
        if form.is_valid():
            form.save()
           # return HttpResponse("Booking created successfully")
            return redirect('dashboard')
    context={'form':form}
    
    return render(request, 'Tour/newbookingForm.html', context)

def newItinerary(request):
    form=ItineraryForm()
    if request.method=='POST':
        form=ItineraryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={'form':form}
    return render(request, 'Tour/newItineraryForm.html', context)

def updateBooking(request,pk):
    booking=Booking.objects.get(id=pk)
    form=BookingForm(instance=booking)
    if request.method=='POST':
        form=BookingForm(request.POST,instance=booking)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={'form':form}
    return render(request,'Tour/newBookingForm.html', context)

def updateItinerary(request,pk):
    itinerary=Itinerary.objects.get(id=pk)
    form=ItineraryForm(instance=itinerary)
    if request.method=='POST':
        form=ItineraryForm(request.POST,instance=itinerary)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={'form':form}
    return render(request,'Tour/newItineraryForm.html', context)

def deleteBooking(request,pk):
    booking=Booking.objects.get(id=pk)
    if request.method=='POST':
        booking.delete()
        return redirect('dashboard')

    context={'obj':booking}
    return render(request, 'Tour/delete.html',context)

def deleteItinerary(request,pk):
    itinerary=Itinerary.objects.get(id=pk)
    if request.method=='POST':
        itinerary.delete()
        return redirect('dashboard')

    context={'obj':itinerary}
    return render(request, 'Tour/delete.html',context)

def profile(request):
    return HttpResponse("This is the profile page")

def room(request):
    return render(request, 'room.html')






# Create your views here.
