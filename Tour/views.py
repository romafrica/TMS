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

def loginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect ('dashboard')
    
     
    if request.method == "POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        
        except:
            messages.error(request, "User does not exist")
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request, "Username or Password is incorrect")    
        


    context={'page':page}
    return render(request, 'Tour/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,"User account created successfully")
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,"An error occured during registration")


    context={'form':form}
    return render(request,'Tour/login_register.html',context)

@login_required(login_url='login')
def dashboard(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    bookings=Booking.objects.filter(
        Q(email__icontains=q) | 
        Q(phone__icontains=q)|
        Q(Original_location__icontains=q)
    )
    itinerary= Itinerary.objects.all()
    context={'bookings':bookings, 'itinerary':itinerary}
    return render(request,'Tour/dashboard.html',context)

@login_required(login_url='login')
def clientList(request):
    bookings=Booking.objects.all()
    context={'bookings':bookings}
    return render(request,'Tour/client_list.html',context)


@login_required(login_url='login')
def clientDetails(request,pk):
    bookings=Booking.objects.get(id=pk)
    context={"bookings":bookings}
    return render(request,'Tour/client_details.html', context)

@login_required(login_url='login')
def itinerary(request):
    itinerary= Itinerary.objects.all()
    context={'itinerary':itinerary}
    return render(request, 'Tour/itinerary.html',context)



@login_required(login_url='login')
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


@login_required(login_url='login')
def newItinerary(request):
    form=ItineraryForm()
    if request.method=='POST':
        form=ItineraryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={'form':form}
    return render(request, 'Tour/newItineraryForm.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteBooking(request,pk):
    booking=Booking.objects.get(id=pk)
    if request.method=='POST':
        booking.delete()
        return redirect('dashboard')

    context={'obj':booking}
    return render(request, 'Tour/delete.html',context)


@login_required(login_url='login')
def deleteItinerary(request,pk):
    itinerary=Itinerary.objects.get(id=pk)
    if request.method=='POST':
        itinerary.delete()
        return redirect('dashboard')

    context={'obj':itinerary}
    return render(request, 'Tour/delete.html',context)


@login_required(login_url='login')
def userProfile(request,pk):
    user=User.objects.get(id=pk)
    context={'user':user}
    return render(request, 'Tour/profile.html',context)








# Create your views here.
