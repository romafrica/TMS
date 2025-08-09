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
from django.forms import modelformset_factory
from .forms import DateRangeForm

#tour/views
from django.contrib.auth.decorators import login_required
from .models import Destination
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import RegisterForm, DestinationForm 
from .forms import ActivityForm, InformationForm
from .forms import DestinationImageForm, RoomForm, RestaurantForm
from .models import Destination
from django.http import JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

import openpyxl
from django.http import HttpResponse


from django.contrib.auth.decorators import login_required
from .models import Destination, Room, DateRange
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render
from .models import Destination  # adjust import based on your app structure

from django.shortcuts import render
from .models import Destination
# tour/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect
from datetime import timedelta


def logout_view(request):
    logout(request)
    return redirect('home') 


def all_destinations(request):
    destinations = Destination.objects.all()
    return render(request, 'tour/all_destinations.html', {'destinations': destinations})

def homepage(request):
    featured_destinations = Destination.objects.all()[:2]
    context = {
        'featured_destinations': featured_destinations
    }
    return render(request, 'tour/home.html', context)


def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'tour/destination_list.html', {'destinations': destinations})


def destination_detail(request, id):
    destination = get_object_or_404(Destination, id=id)
    days = []

    for date_range in destination.date_ranges.all():
        current = date_range.start_date
        while current <= date_range.end_date:
            day_activities = destination.activities.filter(date=current).order_by('start_time')
            days.append({
                'date': current,
                'activities': day_activities
            })
            current += timedelta(days=1)

    tab_labels = ['Gallery', 'Rooms', 'Restaurants', 'Activities and Services', 'Information', 'Map']
    return render(request, 'tour/destination_detail.html', {
        'destination': destination,
        'tab_labels': tab_labels,
        'itinerary_days': days,
    })


# def destination_detail(request, id):
#     destination = get_object_or_404(Destination, id=id)
#     days = []

#     for date_range in destination.date_ranges.all():
#         current = date_range.start_date
#         while current <= date_range.end_date:
#             day_activities = destination.activities.filter(date=current)
#             days.append({
#                 'date': current,
#                 'activities': day_activities
#             })
#             current += timedelta(days=1)

#     tab_labels = ['Gallery', 'Rooms', 'Restaurants', 'Activities and Services', 'Information','Map']
#     return render(request, 'tour/destination_detail.html', {
#         'destination': destination,
#         'tab_labels': tab_labels,
#         'itinerary_days': days,
#     })

# def destination_detail(request, id):
#     destination = get_object_or_404(Destination, id=id)

#     days = []
#     current = destination.start_date
#     while current <= destination.end_date:
#         day_activities = destination.activities.filter(date=current)
#         days.append({
#             'date': current,
#             'activities': day_activities
#         })
#         current += timedelta(days=1)

#     tab_labels = ['Gallery', 'Rooms', 'Restaurants', 'Activities and Services', 'Information','Map']
#     return render(request, 'tour/destination_detail.html', {
#         'destination': destination,
#         'tab_labels': tab_labels,
#         'itinerary_days': days,
#     })





def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard_view(request):
    destinations = request.user.destinations.all()
    return render(request, 'tour/dashboardm.html', {'destinations': destinations})


# @login_required
def add_destination_view(request):
    DateRangeFormSet = modelformset_factory(DateRange, form=DateRangeForm, extra=1)

    if request.method == 'POST':
        form = DestinationForm(request.POST)
        formset = DateRangeFormSet(request.POST, queryset=DateRange.objects.none())
        
        if form.is_valid() and formset.is_valid():
            dest = form.save(commit=False)
            dest.user = request.user
            dest.save()

            for subform in formset:
                if subform.cleaned_data:
                    date_range = subform.save(commit=False)
                    date_range.destination = dest
                    date_range.save()

            return redirect('dashboard')
    else:
        form = DestinationForm()
        formset = DateRangeFormSet(queryset=DateRange.objects.none())

    return render(request, 'Tour/add_destination.html', {
        'form': form,
        'date_formset': formset,
    })


# @login_required
# def add_destination_view(request):
#     if request.method == 'POST':
#         form = DestinationForm(request.POST)
#         if form.is_valid():
#             dest = form.save(commit=False)
#             dest.user = request.user
#             dest.save()
#             return redirect('dashboard')
#     else:
#         form = DestinationForm()
#     return render(request, 'tour/add_destination.html', {'form': form})



@login_required
def upload_images(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)

    if request.method == 'POST':
        img_form = DestinationImageForm(request.POST, request.FILES)
        if img_form.is_valid():
            image = img_form.save(commit=False)
            image.destination = destination
            image.save()
            return redirect('destination_detail', id=destination.id)
    else:
        img_form = DestinationImageForm()
    
    return render(request, 'tour/upload_image.html', {'form': img_form, 'destination': destination})

@login_required
def upload_gallery_image(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)
    if request.method == 'POST':
        form = DestinationImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.destination = destination
            image.save()
            return redirect('destination_detail', id=destination.id)
    else:
        form = DestinationImageForm()
    return render(request, 'tour/upload_image.html', {'form': form, 'title': 'Upload Gallery Image'})

@login_required
def upload_room(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.destination = destination
            room.save()
            return redirect('destination_detail', id=destination.id)
    else:
        form = RoomForm()
    return render(request, 'tour/upload_image.html', {'form': form, 'title': 'Add Room'})

@login_required
def upload_restaurant(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.destination = destination
            restaurant.save()
            return redirect('destination_detail', id=destination.id)
    else:
        form = RestaurantForm()
    return render(request, 'tour/upload_image.html', {'form': form, 'title': 'Add Restaurant'})

@login_required
def edit_destination(request, id):
    destination = get_object_or_404(Destination, id=id, user=request.user)
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'tour/edit_destination.html', {'form': form, 'destination': destination})

@login_required
def delete_destination(request, id):
    destination = get_object_or_404(Destination, id=id, user=request.user)
    if request.method == 'POST':
        destination.delete()
        return redirect('dashboard')
    return render(request, 'tour/delete_destination.html', {'destination': destination})




@login_required
def upload_activity(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.destination = destination
            activity.save()
            return redirect('destination_detail', id=destination.id)
    else:
        form = ActivityForm()

    return render(request, 'tour/upload_activity.html', {
        'form': form,
        'title': 'Add Activity',
        'destination': destination,
    })


       
@login_required
def upload_information(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)
    if request.method == 'POST':
        form = InformationForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.destination = destination
            info.save()
            return redirect('destination_detail', id=destination.id)
    else:
        form = InformationForm()
    return render(request, 'tour/upload_information.html', {'form': form, 'title': 'Add Info', 'destination': destination})




@login_required
def accommodation_summary_view(request):
    client = request.user

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Parse the date strings if they exist
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None

    # Get all destinations for the client
    destinations = Destination.objects.filter(user=client).prefetch_related('rooms', 'daterange_set')

    summary = []
    grand_total = 0

    for destination in destinations:
        # Filter date ranges based on input (if any)
        date_ranges = destination.daterange_set.all()
        if start_date:
            date_ranges = date_ranges.filter(end_date__gte=start_date)
        if end_date:
            date_ranges = date_ranges.filter(start_date__lte=end_date)

        for date_range in date_ranges:
            destination_total = 0
            for room in destination.rooms.all():
                room_cost = room.cost * room.nights
                summary.append({
                    'start_date': date_range.start_date,
                    'end_date': date_range.end_date,
                    'destination': destination.name,
                    'accommodation': room.name,
                    'basis': room.basis,
                    'nights': room.nights,
                    'cost': room.cost,
                    'total_cost': room_cost,
                })
                destination_total += room_cost
            grand_total += destination_total

    return render(request, 'tour/accommodation_summary.html', {
        'summary': summary,
        'grand_total': grand_total,
        'start_date': start_date_str,
        'end_date': end_date_str,
    })

# @login_required
# def accommodation_summary_view(request):
#     client = request.user

#     start_date_str = request.GET.get('start_date')
#     end_date_str = request.GET.get('end_date')
    
    

#     destinations = Destination.objects.filter(user=client).prefetch_related('rooms')
#     if start_date_str:
#         start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
#         destinations = destinations.filter(start_date__gte=start_date)

#     if end_date_str:
#         end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
#         destinations = destinations.filter(end_date__lte=end_date)

#     summary = []
#     grand_total = 0

#     for destination in destinations:
#         destination_total = 0
#         for room in destination.rooms.all():
#             room_cost = room.cost * room.nights
#             summary.append({
#                 'start_date': destination.start_date,
#                 'end_date': destination.end_date,
#                 'destination': destination.name,
#                 'accommodation': room.name,
#                 'basis': room.basis,
#                 'nights': room.nights,
#                 'cost': room.cost,
#                 'total_cost': room_cost,
#             })
#             destination_total += room_cost
#         grand_total += destination_total

#     return render(request, 'tour/accommodation_summary.html', {
#         'summary': summary,
#         'grand_total': grand_total,
#         'start_date': start_date_str,
#         'end_date': end_date_str,
#     })


@login_required
def export_summary_excel(request):
    user = request.user
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Parse dates
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None

    destinations = Destination.objects.filter(user=user).prefetch_related('rooms', 'daterange_set')

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Accommodation Summary'
    headers = ['Start Date', 'End Date', 'Destination', 'Room', 'Basis', 'Nights', 'Cost', 'Total Cost']
    sheet.append(headers)

    for dest in destinations:
        date_ranges = dest.daterange_set.all()
        if start_date:
            date_ranges = date_ranges.filter(end_date__gte=start_date)
        if end_date:
            date_ranges = date_ranges.filter(start_date__lte=end_date)

        for dr in date_ranges:
            for room in dest.rooms.all():
                total = room.cost * room.nights
                sheet.append([
                    dr.start_date,
                    dr.end_date,
                    dest.name,
                    room.name,
                    room.basis,
                    room.nights,
                    float(room.cost),
                    float(total)
                ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=accommodation_summary.xlsx'
    workbook.save(response)
    return response


@login_required
def export_summary_pdf(request):
    from django.template.loader import get_template
    from xhtml2pdf import pisa
    from django.http import HttpResponse
    from datetime import datetime
    from .models import Destination

    user = request.user
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None

    destinations = Destination.objects.filter(user=user).prefetch_related('rooms', 'date_ranges')

    summary = []

    for destination in destinations:
        date_ranges = destination.date_ranges.all()
        if start_date:
            date_ranges = date_ranges.filter(end_date__gte=start_date)
        if end_date:
            date_ranges = date_ranges.filter(start_date__lte=end_date)

        for date_range in date_ranges:
            for room in destination.rooms.all():
                summary.append({
                    'start_date': date_range.start_date,
                    'end_date': date_range.end_date,
                    'destination': destination.name,
                    'accommodation': room.name,
                    'basis': room.basis,
                    'nights': room.nights,
                    'cost': room.cost,
                    'total_cost': room.cost * room.nights,
                })

    template = get_template('tour/summary_pdf_template.html')
    html = template.render({'summary': summary})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="accommodation_summary.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response


# @login_required
# def export_summary_pdf(request):
#     user = request.user
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     destinations = Destination.objects.filter(user=user).prefetch_related('rooms')
#     if start_date:
#         destinations = destinations.filter(start_date__gte=start_date)
#     if end_date:
#         destinations = destinations.filter(end_date__lte=end_date)

#     summary = []
#     for destination in destinations:
#         for room in destination.rooms.all():
#             summary.append({
#                 'start_date': destination.start_date,
#                 'end_date': destination.end_date,
#                 'destination': destination.name,
#                 'accommodation': room.name,
#                 'basis': room.basis,
#                 'nights': room.nights,
#                 'cost': room.cost,
#                 'total_cost': room.cost * room.nights,
#             })

#     template = get_template('tour/summary_pdf_template.html')
#     html = template.render({'summary': summary})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="accommodation_summary.pdf"'

#     pisa.CreatePDF(html, dest=response)
#     return response

from django.shortcuts import render
from .models import Destination
from datetime import timedelta

from django.db.models import Sum
# utils.py or at the top of views.py
def get_accommodation_summary(destinations, start_date=None, end_date=None):
    summary = []

    for destination in destinations:
        date_ranges = destination.date_ranges.all()
        if start_date:
            date_ranges = date_ranges.filter(end_date__gte=start_date)
        if end_date:
            date_ranges = date_ranges.filter(start_date__lte=end_date)

        for date_range in date_ranges:
            for room in destination.rooms.all():
                summary.append({
                    'start_date': date_range.start_date,
                    'end_date': date_range.end_date,
                    'destination': destination.name,
                    'accommodation': room.name,
                    'basis': room.basis,
                    'nights': room.nights,
                    'cost': room.cost,
                    'total_cost': room.cost * room.nights,
                })
    return summary


# def get_accommodation_summary(destinations):
#     summary = []
#     for destination in destinations:
#         for room in destination.rooms.all():
#             summary.append({
#                 'start_date': destination.start_date,
#                 'end_date': destination.end_date,
#                 'destination': destination.name,
#                 'accommodation': room.name,
#                 'basis': room.basis,
#                 'nights': room.nights,
#                 'cost': room.cost,
#                 'total_cost': room.cost * room.nights,
#             })
#     return summary


# def public_dashboard_view(request):
#     destinations = Destination.objects.all()[:2]

#     for dest in destinations:
#         days = []
#         for date_range in dest.date_ranges.all():
#             current = date_range.start_date
#             while current <= date_range.end_date:
#                 activities = dest.activities.filter(date=current)
#                 days.append({'date': current, 'activities': activities})
#                 current += timedelta(days=1)
#         dest.itinerary_days = days
#         totals = dest.rooms.aggregate(
#             total_nights=Sum('nights'),
#             total_cost=Sum('cost')
#         )
#         dest.total_nights = totals['total_nights'] or 0
#         dest.total_cost = totals['total_cost'] or 0

#     summary = get_accommodation_summary(destinations)

#     return render(request, 'tour/public_dashboard.html', {
#         'destinations': destinations,
#         'summary': summary,
#     })


def public_dashboard_view(request):
    destinations = Destination.objects.all().prefetch_related('rooms', 'date_ranges', 'activities')[:2]

    for dest in destinations:
        days = []
        for date_range in dest.date_ranges.all():
            current = date_range.start_date
            while current <= date_range.end_date:
                activities = dest.activities.filter(date=current)
                days.append({'date': current, 'activities': activities})
                current += timedelta(days=1)
        dest.itinerary_days = days
        totals = dest.rooms.aggregate(
            total_nights=Sum('nights'),
            total_cost=Sum('cost')
        )
        dest.total_nights = totals['total_nights'] or 0
        dest.total_cost = totals['total_cost'] or 0

    summary = get_accommodation_summary(destinations)
    return render(request, 'tour/public_dashboard.html', {
        'destinations': destinations,
        'summary': summary,
    })



def get_travel_dates(request, destination_id):
    date_ranges = DateRange.objects.filter(destination_id=destination_id)
    dates = []

    for dr in date_ranges:
        current = dr.start_date
        while current <= dr.end_date:
            dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)

    return JsonResponse({'dates': dates})







def home(request,):
    return render(request, 'tour/home.html',)



# def loginPage(request):
#     page='login'

#     if request.user.is_authenticated:
#         return redirect ('dashboard')
    
     
#     if request.method == "POST":
#         username=request.POST.get('username').lower()
#         password=request.POST.get('password')
#         try:
#             user=User.objects.get(username=username)
        
#         except:
#             messages.error(request, "User does not exist")
#         user=authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request,user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, "Username or Password is incorrect")    
        


#     context={'page':page}
#     return render(request, 'Tour/login_register.html',context)

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, 'Tour/login_register.html', {'page': page})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, "Username or Password is incorrect")    

    return render(request, 'tour/login_register.html', {'page': page})


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
    return render(request,'tour/dashboard.html',context)

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

    return render(request, 'Tour/newBookingForm.html', context)

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
