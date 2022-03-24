from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.

def welcome(request): 
    """Shows the main page"""    
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM available ORDER BY library")
        available = cursor.fetchall()
        
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM available ORDER BY library")
        total_space_available = cursor.fetchall()
        
    result_dict = {'records': available, 'records_total': total_space_available}    
    
    return render(request, 'gotspaceanot/welcome.html', result_dict)


def library_system_records(request):
    """Shows the main page"""    
    
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM library_system ORDER BY library")
        library_system = cursor.fetchall()
        
    result_dict_2 = {'records_library': library_system}    

    return render(request, "gotspaceanot/library_system_records.html", result_dict_2)

def about(request):
    return render(request, 'gotspaceanot/about.html')

def login(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if martic_number is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM student WHERE matric_number = %s", [request.POST['Matric Number']])
            student = cursor.fetchone()
            ## No student with same matric card
            if student == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO student VALUES (%s, %s, %s, %s)"
                        , [request.POST['Matric Number'], request.POST['Email'], request.POST['Library'], request.POST['Level']])
                ##Updating the available space when a student register which level he is going to study 
                cursor.execute("UPDATE available SET available_seats = available_seats - 1 WHERE (library,level) =  (%s, %s)", [request.POST['Library'],request.POST['Level']] )
                
                return redirect('gotspaceanot-logout') 
            else:
                status = 'Student with Matric Number %s already exists' % (request.POST['Matric Number'])


    context['status'] = status
 
    return render(request, "gotspaceanot/login.html", context)

def logout(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if matric_number is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM student WHERE matric_number = %s", [request.POST['Matric Number']])
            student = cursor.fetchone()
            ## No student with same matric card
            if student == None:
                status = 'Student with Matric Number %s does not exists' % (request.POST['Matric Number'])
            else:
                ##Updating the available space when a student logsout
                cursor.execute("UPDATE available SET available_seats = available_seats + 1 WHERE (library,Level) = (%s, %s)", [student[2] , student[3]])
                cursor.execute("DELETE FROM student WHERE matric_number = (%s)", [request.POST['Matric Number']])
                cursor.execute("DELETE FROM library_system WHERE matric_number = (%s)", [request.POST['Matric Number']])
                
                return redirect('gotspaceanot-welcome') 

    context['status'] = status
 
    return render(request, "gotspaceanot/logout.html", context)

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
                cursor.execute("INSERT INTO library_system VALUES (%s, %s, %s)"
                        , [request.POST['Matric Number'], request.POST['Email'], request.POST['Library'] ])
                return redirect('gotspaceanot-welcome')    
            else:
                status = 'Student with Matric Number %s already inside the library' % (request.POST['Matric Number'])


    context['status'] = status
 
    return render(request, "gotspaceanot/library_system.html", context)   
