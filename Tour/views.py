from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import *


def home(request,):
    
    return render(request, 'Tour/home.html',)



def logoutUser(request):
    logout(request)
    return redirect('home')

