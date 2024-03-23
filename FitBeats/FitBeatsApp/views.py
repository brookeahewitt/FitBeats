from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, 'index.html')

def exercises(request):
    return render(request, 'exercises.html')