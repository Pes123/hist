# myapp/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Укажите путь к вашему шаблону