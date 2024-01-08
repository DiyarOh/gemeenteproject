from django.urls import path
from .views import ComplaintsFormView


urlpatterns = [
    path('klachtenformulier/', ComplaintsFormView.as_view(), name='complaints_form'),
]
