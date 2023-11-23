from django.urls import path
from . import views

app_name = 'visitors'



urlpatterns = [
    path('visitor-log/', views.visitor_log, name='visitor-log'),
]