# urls.py
from django.urls import path
from .views import ComplaintsFormView, ComplaintsDashboard, KlachtMapView, KlachtDetailView, KlachtDeleteView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('klachtformulier/', ComplaintsFormView.as_view(), name='complaints_form'),
    path('dashboard/', login_required(ComplaintsDashboard.as_view()), name='complaints_dashboard'),
    path('kaart/', login_required(KlachtMapView.as_view()), name='kaart'),
    path('detail/<int:pk>/', login_required(KlachtDetailView.as_view()), name='klacht'),
    path('klacht/<int:pk>/delete/', login_required(KlachtDeleteView.as_view()), name='klacht_delete'),

    # If you have other URL patterns, add them here
]
