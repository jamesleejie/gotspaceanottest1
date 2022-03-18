from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'gotspaceanot-home'),
    path('about/', views.about, name='gotspaceanot-about'),
]
