#tour/models
from django.db import models
from django.db import models
from django.contrib.auth.models import User

# DESTINATION_CHOICES = [
#         ('KISUMU', 'Kisumu'),
#         ('MOMBASA', 'Mombasa'),
#         ('NAIROBI', 'Nairobi'),
       
#     ]
class Destination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destinations')
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    map_embed_code = models.TextField(help_text="Embed iframe from Google Maps")

    def __str__(self):
        return self.name



class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='destination_gallery/')

class Room(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='rooms/')

class Restaurant(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurants/')



class Activity(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=100)
    description = models.TextField()

class Information(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='info')
    content = models.TextField()
