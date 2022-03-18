from django.shortcuts import render

# Create your views here.

library_system = [
    {
        'Library': 'CLB',
        'Level': '3',
        'Total_Space': '50',
        'Available_Space': '50',
    },
    {
        'Library': 'SLB',
        'Level': '4',
        'Total_Space': '20',
        'Available_Space': '20',
    }
]


def home(request):
    context = {
        'library_system': library_system
    }
    return render(request, 'gotspaceanot/home.html', context)


def about(request):
    return render(request, 'gotspaceanot/about.html')
