from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports, name="reports"),
    path('systemReports', views.systemReports, name="systemReports"),
    path('schoolReports', views.schoolReports, name="schoolReports"),
    
]
