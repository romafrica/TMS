from django.contrib import admin
from .models import Destination, DestinationImage, Room, Restaurant, Activity, Information

admin.site.register(Destination)
admin.site.register(DestinationImage)
admin.site.register(Room)
admin.site.register(Restaurant)
admin.site.register(Activity)
admin.site.register(Information)
