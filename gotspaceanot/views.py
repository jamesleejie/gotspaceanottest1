from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def administrator(request):
    ## Delete student
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM student WHERE matric_number = %s", [request.POST['Matric Number']])    
                
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM student ORDER BY library")
        student = cursor.fetchall()   
        
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM library_system ORDER BY library")
        library_system = cursor.fetchall()    
        
    result_dict = {'library_system': library_system, 'student':student }
    
    return render(request, 'gotspaceanot/administrator.html',result_dict)

def welcome(request): 
    """Shows the main page"""    
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM available ORDER BY library")
        available = cursor.fetchall()
        
    with connection.cursor() as cursor:
        cursor.execute("SELECT library, SUM(available_seats) as Total_Available_Seats, SUM(total_seats) as Total_Space FROM available GROUP BY library ORDER BY library ASC")
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

def nus_system(request):
    """Shows the main page"""    
    
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM nus_system")
        nus_system = cursor.fetchall()
        
    result_dict_2 = {'records_nus': nus_system}    

    return render(request, "gotspaceanot/nus_system.html", result_dict_2)

def about(request):
    return render(request, 'gotspaceanot/about.html')

def login(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if martic_number is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM library_system WHERE matric_number = %s", [request.POST['Matric Number']])
            lib = cursor.fetchone()
            cursor.execute("SELECT * FROM student WHERE matric_number = %s", [request.POST['Matric Number']])
            student = cursor.fetchone()
            ## No student with same matric card
            if lib[4] == lib[3]:
                cursor.execute("INSERT INTO student VALUES (%s, %s, %s, %s)"
                        , [request.POST['Matric Number'], request.POST['Email'], request.POST['Library'], request.POST['Level']])
                ##Updating the available space when a student register which level he is going to study 
                cursor.execute("UPDATE available SET available_seats = available_seats - 1 WHERE (library,level) =  (%s, %s)", [request.POST['Library'],request.POST['Level']] )
                return redirect('gotspaceanot-logout')            
            else:
                status = 'Student with Matric Number %s already exists and have not logged out.' % (request.POST['Matric Number'])                


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
                cursor.execute("UPDATE available SET available_seats = available_seats + 1 WHERE library = %s and Level = %s ", [student[2] , student[3]])
                cursor.execute("UPDATE student SET time_exited = Now() WHERE DATE(Now()) = %s", [SELECT CURRENT_DATE()])
                cursor.execute("UPDATE library_system SET time_exited = Now() WHERE DATE(Now()) = %s", [SELECT CURRENT_DATE()])
                return redirect('gotspaceanot-welcome') 

    context['status'] = status
 
    return render(request, "gotspaceanot/logout.html", context)

def library_system(request):
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM NUS_system WHERE matric_number = %s", [request.POST['Matric Number']])
            NUS_system = cursor.fetchone()
            cursor.execute("SELECT * FROM library_system WHERE matric_number = %s", [request.POST['Matric Number']])
            library_system = cursor.fetchone()
            ## No customer with same id
            if NUS_system == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO NUS_system VALUES (%s, %s)"
                        , [request.POST['Matric Number'], request.POST['Email']])
                
            if library_system == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO library_system VALUES (%s, %s, %s)"
                        , [request.POST['Matric Number'], request.POST['Email'], request.POST['Library'] ])
                return redirect('gotspaceanot-welcome')    
            else:
                status = 'Student with Matric Number %s already inside the library' % (request.POST['Matric Number'])

    context['status'] = status
 
    return render(request, "gotspaceanot/library_system.html", context)   

def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM student  WHERE matric_number = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE NUS_system SET matric_number = %s, email = %s WHERE matric_number = %s"
                    , [request.POST['matric_number'], request.POST['email'], id ])            
            cursor.execute("UPDATE student SET matric_number = %s, email = %s, library = %s, Level = %s WHERE matric_number = %s"
                    , [request.POST['matric_number'], request.POST['email'], request.POST['library'],
                        request.POST['Level'] , id ])   
            cursor.execute("UPDATE available SET available_seats = available_seats + 1 WHERE (library,level) =  (%s, %s)", [obj[2],obj[3]] )
            cursor.execute("UPDATE available SET available_seats = available_seats - 1 WHERE (library,level) =  (%s, %s)", [request.POST['library'],request.POST['Level']] )
            status = 'Student details edited successfully!'
            cursor.execute("SELECT * FROM student WHERE matric_number = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "gotspaceanot/edit.html", context)
