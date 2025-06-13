from django.contrib.auth.models import User
from django.db import models
from datetime import date


class Booking(models.Model):
    first_name=models.CharField(max_length=100,default='Unknown')
    last_name=models.CharField(max_length=100,  default='Unknown')
    email=models.EmailField(max_length=100, default='default@example.com')
    phone=models.CharField(max_length=100,  default='0000000000')
    Original_location=models.CharField(max_length=100, default='Unknown')
    destination=models.CharField(max_length=100, default='Unknown')
    departure_date=models.DateField(default='2025-01-01')
    return_date=models.DateField(default='2025-01-01')
    created_at= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at= models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering= ['-updated_at', '-created_at']

    def __str__(self):
        return self.first_name + ' ' + self.last_name 
    



class Itinerary(models.Model):
    first_name=models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    location=models.CharField(max_length=100, default='Unknown')
    activity=models.TextField()
    cost=models.DecimalField(max_digits=10, decimal_places=2 ) 
    date=models.DateField(default='2025-01-01')
   # time=models.TimeField()  
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering= ['updated_at','-created_at']
    

    def __str__(self):
        return self.location




