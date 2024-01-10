from django.urls import path
from .views import ComplaintsFormView, ComplaintsDashboard


urlpatterns = [
    path('klachtenformulier/', ComplaintsFormView.as_view(), name='complaints_form'),
    path('dashboard/', ComplaintsDashboard.as_view(), name='complaints_dashboard'),
]
