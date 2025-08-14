from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import Booking, Destination, Activity, Stay, DiningExpense, TravelLeg


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["client", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


# --- Inline formset: Booking -> Destination
DestinationFormSet = inlineformset_factory(
    Booking,
    Destination,
    fields=["name", "start_date", "end_date"],
    widgets={
        "start_date": forms.DateInput(attrs={"type": "date"}),
        "end_date": forms.DateInput(attrs={"type": "date"}),
    },
    extra=1,
    can_delete=True,
)


# Helpers: destination-scoped ModelForms that accept a restricted queryset
class _DestinationScopedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        dest_qs = kwargs.pop("dest_qs", None)
        super().__init__(*args, **kwargs)
        if "destination" in self.fields and dest_qs is not None:
            self.fields["destination"].queryset = dest_qs


class ActivityForm(_DestinationScopedForm):
    class Meta:
        model = Activity
        fields = ["destination", "name", "date", "start_time", "end_time", "cost"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }


class StayForm(_DestinationScopedForm):
    class Meta:
        model = Stay
        fields = ["destination", "hotel_name", "nightly_rate", "nights", "rooms", "basis"]


class DiningExpenseForm(_DestinationScopedForm):
    class Meta:
        model = DiningExpense
        fields = ["destination", "restaurant", "date", "description", "cost"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


# ModelFormSets for destination-children (each row chooses a Destination)
ActivityFormSet = modelformset_factory(
    Activity, form=ActivityForm, extra=1, can_delete=True
)

StayFormSet = modelformset_factory(
    Stay, form=StayForm, extra=1, can_delete=True
)

DiningExpenseFormSet = modelformset_factory(
    DiningExpense, form=DiningExpenseForm, extra=1, can_delete=True
)


# Inline formset: Booking -> TravelLeg
class TravelLegForm(forms.ModelForm):
    class Meta:
        model = TravelLeg
        fields = [
            "mode",
            "date",
            "from_location",
            "to_location",
            "from_destination",
            "to_destination",
            "cost",
        ]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


TravelLegFormSet = inlineformset_factory(
    Booking,
    TravelLeg,
    form=TravelLegForm,
    extra=1,
    can_delete=True,
)
