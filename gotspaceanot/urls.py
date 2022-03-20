from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name = 'gotspaceanot-welcome'),
    path('library_system_records/', views.library_system_records, name = 'gotspaceanot-library_system_records'),
    path('about/', views.about, name='gotspaceanot-about'),
    path('login/', views.login, name = 'gotspaceanot-login'),
    path('add/' , views.add, name = 'gotspaceanot-add'),
    path('library_system/', views.library_system, name = 'gotspaceanot-library_system'),
]
