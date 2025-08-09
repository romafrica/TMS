from django.forms import ModelForm
from .models import Booking, Itinerary
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Destination, DestinationImage, Room, Restaurant, Activity, Information  
from django import forms
from .models import Destination, DateRange
from .models import DestinationImage, Room, Restaurant
from .models import DestinationImage, Room, Restaurant
from django import forms
from .models import Activity

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'country', 'description', 'map_embed_code']

class DateRangeForm(forms.ModelForm):
    class Meta:
        model = DateRange
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date cannot be after end date.")


# class DestinationForm(forms.ModelForm):
#     class Meta:
#         model = Destination
#         fields = ['name', 'country', 'start_date', 'end_date', 'description', 'map_embed_code']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date'}),
#             'end_date': forms.DateInput(attrs={'type': 'date'}),
#         }
#     def clean(self):
#         cleaned_data = super().clean()
#         start_date = cleaned_data.get("start_date")
#         end_date = cleaned_data.get("end_date")

#         if start_date and end_date and start_date > end_date:
#             raise forms.ValidationError("Start date cannot be after end date.")




class DestinationImageForm(forms.ModelForm):
    class Meta:
        model = DestinationImage
        fields = ['image']



class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'image', 'cost', 'basis', 'nights']
        labels = {
            'name': 'Room Name',
            'description': 'Room Description',
            'image': 'Room Image',
            'cost': 'Accommodation Cost (KSh)',
            'basis': 'Basis (FB/HB/BB)',
            'nights': 'Number of Nights',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'image']
        


class DestinationImageForm(forms.ModelForm):
    class Meta:
        model = DestinationImage
        fields = ['image']


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'image']  

class DateRangeForm(forms.ModelForm):
    class Meta:
        model = DateRange
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date cannot be after end date.")



class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['destination', 'title', 'description', 'date', 'start_time', 'end_time']  # only field names here
        widgets = {
            'destination': forms.Select(attrs={'id': 'destinationSelect'}),
            'date': forms.DateInput(attrs={'type': 'date', 'id': 'dateInput'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        destination = cleaned_data.get('destination')
        date = cleaned_data.get('date')

        if destination and date:
            valid_dates = destination.get_valid_dates()
            if date not in valid_dates:
                raise forms.ValidationError(
                    f"The date {date} is not within the allowed travel dates for {destination.name}."
                )


class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['content']

class BookingForm(ModelForm):
    class Meta:
        model=Booking
        fields='__all__'

class ItineraryForm(ModelForm):
    class Meta:
        model=Itinerary
        fields='__all__'