from django.shortcuts import render

# Create your views here.

library_system = [
    {
        'Library': 'CLB',
        'Level': '3',
      
    },
    {
        'Library': 'SLB',
        'Level': '4',
        'Available_Space': '20',
        'Total_Space': '20',  
    }
]

def welcome(request): 
    return render(request, "gotspaceanot/welcome.html")

def home(request):
    context = {
        'library_system': library_system
    }
    return render(request, 'gotspaceanot/home.html', context)

def about(request):
    return render(request, 'gotspaceanot/about.html')

def login(request):
    return render(request, 'gotspaceanot/login.html')
