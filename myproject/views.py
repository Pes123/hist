# myapp/views.py
from pyexpat.errors import messages
import random
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from myproject import settings

def home(request):
    return render(request, 'home.html')  


