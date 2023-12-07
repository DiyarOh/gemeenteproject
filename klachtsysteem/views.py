from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views import View

# Create your views here.
class ComplaintsFormView(TemplateView):
    template_name = "klachtenformulier.html"

class HomePageView(TemplateView):
    template_name = "homepage.html"

class DashboardView(TemplateView):
    template_name = "dashboard.html"

class KlachtBeheerView(TemplateView):
    template_name = "klachtbeheer.html"

class KlachtMapView(TemplateView):
    template_name = "klachtmap.html"

class LoginView(TemplateView):
    template_name = "login.html"

class RegisterView(TemplateView):
    template_name = "register.html"