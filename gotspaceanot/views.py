from django.shortcuts import render

# Create your views here.

library_system = [
    {
        'Library': 'CLB',
        'Level': '3',
        'Available_Space': '50',
        'Total_Space': '50',  
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
    """Shows the main page"""    
    context = {
        'library_system': library_system
    }
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM context ORDER BY Library")
        library = cursor.fetchall()    
    return render(request, 'gotspaceanot/home.html', context)

def about(request):
    return render(request, 'gotspaceanot/about.html')

def login(request):
    return render(request, 'gotspaceanot/login.html')
