from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.

def welcome(request): 
    """Shows the main page"""    
    
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM available ORDER BY library")
        available = cursor.fetchall()
        
    result_dict = {'records': available}
    return render(request, "gotspaceanot/welcome.html", result_dict)

def home(request):
    """Shows the main page"""    
    
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM available ORDER BY library")
        available = cursor.fetchall()
        
    result_dict = {'records': available}

    return render(request, 'gotspaceanot/home.html', result_dict)

def about(request):
    return render(request, 'gotspaceanot/about.html')

def login(request):
    return render(request, 'gotspaceanot/login.html')
