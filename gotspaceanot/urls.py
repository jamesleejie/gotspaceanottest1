from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'GotSpaceAnot-home'),
    path('about/', views.about, name='GotSpaceAnot-about'),
]