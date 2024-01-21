# urls.py
from django.urls import path
from .views import ComplaintsFormView, ComplaintsDashboard, KlachtMapView

urlpatterns = [
    path('klachtformulier/', ComplaintsFormView.as_view(), name='complaints_form'),
    path('dashboard/', ComplaintsDashboard.as_view(), name='complaints_dashboard'),
    path('kaart/', KlachtMapView.as_view(), name='kaart'),
    # If you have other URL patterns, add them here
]
