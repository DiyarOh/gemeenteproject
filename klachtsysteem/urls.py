
from django.contrib import admin
from django.urls import path
from .views import (
    ComplaintsFormView,
    HomePageView,
    DashboardView,
    KlachtBeheerView,
    KlachtMapView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('klachtenformulier/', ComplaintsFormView.as_view(), name='complaints_form'),
]
