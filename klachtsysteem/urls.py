# urls.py
from django.urls import path
from .views import ComplaintsFormView, ComplaintsDashboard, submit_klacht

urlpatterns = [
    path('klachtformulier/', ComplaintsFormView.as_view(), name='complaints_form'),
    path('dashboard/', ComplaintsDashboard.as_view(), name='complaints_dashboard'),
    path('submit_klacht/', submit_klacht, name='submit_klacht'), 
    # If you have other URL patterns, add them here
]
