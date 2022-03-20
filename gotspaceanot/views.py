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

def library_system(request):
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM library_system WHERE matric_number = %s", [request.POST['Matric Number']])
            library_system = cursor.fetchone()
            ## No customer with same id
            if library_system == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO library_system VALUES (%s, %s)"
                        , [request.POST['Matric Number'], request.POST['Email'], request.POST['Library'] ])
                return redirect('welcome')    
            else:
                status = 'Student with Matric Number %s already inside the library' % (request.POST['Matric Number'])


    context['status'] = status
 
    return render(request, "gotspaceanot/library_system.html", context)   

def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM student WHERE matric_number = %s", [request.POST['Matric Number']])
            student = cursor.fetchone()
            ## No customer with same id
            if student == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO student VALUES (%s, %s)"
                        , [request.POST['Matric Number'], request.POST['Email'] ])
                return redirect('welcome')    
            else:
                status = 'Student with Matric Number %s already exists' % (request.POST['Matric Number'])


    context['status'] = status
 
    return render(request, "gotspaceanot/add.html", context)
