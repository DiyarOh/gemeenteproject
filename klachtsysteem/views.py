# views.py
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .utils import is_valid_invitation_code 
from .models import Invitation, Klacht, Status
from .forms import ComplaintSearchForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as geomodels
from django.http import JsonResponse
from django.utils import timezone

# Make sure to import Status model
from .models import Klacht, Status

# Login view
def login_view(request):
    # Redirect to complaints_dashboard if already authenticated
    if request.user.is_authenticated:
        return redirect('complaints_dashboard') 

    # Handle login form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # If user is authenticated, login and redirect
        if user is not None:
            login(request, user)
            return redirect('complaints_dashboard')
        else:
            return render(request, 'login.html', {'errors': ['Invalid credentials']})

    # Render login page for GET request
    return render(request, 'login.html')

# Register view
def register_view(request, invitation_code=None):
    # Redirect to complaints_dashboard if already authenticated
    if request.user.is_authenticated:
        return redirect('complaints_dashboard') 

    # Redirect to invalid_code if invitation is invalid
    if invitation_code is None or not is_valid_invitation_code(invitation_code) or invitation_code == '':
        return redirect('invalid_code')

    # Handle registration form submission
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            invitation = Invitation.objects.get(code=invitation_code)
            invitation.is_used = True
            invitation.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    # Render registration page
    return render(request, 'register.html', {'form': form, 'invitation_code': invitation_code})

# Invalid code view
def invalid_code_view(request):
    # Redirect to complaints_dashboard if already authenticated
    if request.user.is_authenticated:
        return redirect('complaints_dashboard') 

    # Render invalid_code page
    return render(request, 'invalid_code.html')

# Logout view
def logout_view(request):
    # Logout and redirect to login
    logout(request)
    return redirect('login')

# Complaints form view
class ComplaintsFormView(TemplateView):
    template_name = "klachtformulier.html"

# Home page view
class HomePageView(TemplateView):
    template_name = "homepage.html"

# Complaints dashboard view
class ComplaintsDashboard(ListView):
    model = Klacht
    template_name = 'klachtbeheer.html'
    context_object_name = 'klachten'
    paginate_by = 5

    def get_queryset(self):
        # Retrieve filter parameters from request
        search_query = self.request.GET.get('search_query')
        search_desc = self.request.GET.get('search_desc')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')

        # Retrieve all complaints and order by submission date
        queryset = Klacht.objects.all()
        queryset = queryset.order_by('datum_melding')

        # Apply filters based on parameters
        if search_query:
            queryset = queryset.filter(naam__icontains=search_query)

        if search_desc:
            queryset = queryset.filter(omschrijving__icontains=search_desc)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            queryset = queryset.filter(datum_melding__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            queryset = queryset.filter(datum_melding__lte=end_date)

        if status:
            queryset = queryset.filter(status__id=status)

        return queryset

    def get_context_data(self, **kwargs):
        # Retrieve filtered queryset
        filtered_queryset = self.get_queryset()
        
        # Paginate the results
        paginator = Paginator(filtered_queryset, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            klachten = paginator.page(page)
        except PageNotAnInteger:
            klachten = paginator.page(1)
        except EmptyPage:
            klachten = paginator.page(paginator.num_pages)

        # Prepare context data
        context = super(ComplaintsDashboard, self).get_context_data(**kwargs)
        context[self.context_object_name] = klachten
        context['search_form'] = ComplaintSearchForm(self.request.GET)
        context['statuses'] = Status.objects.all()

        return context

# Submit klacht view
def submit_klacht(request):
    if request.method == 'POST':
        # Retrieve form data
        naam = request.POST.get('naam')
        omschrijving = request.POST.get('omschrijving')
        email = request.POST.get('email')
        longitude_str = request.POST.get('longitude')
        latitude_str = request.POST.get('latitude')

        # Check if longitude and latitude are provided
        if longitude_str is not None and latitude_str is not None:
            try:
                longitude = float(longitude_str)
                latitude = float(latitude_str)
            except ValueError:
                return JsonResponse({'error': 'Invalid longitude or latitude format'}, status=400)

            # Get or create the Status object with ID 1
            status, created = Status.objects.get_or_create(id=1, defaults={'waarde': 'Default', 'beschrijving': 'Default status'})

            # Create Klacht object
            klacht = Klacht(
                naam=naam,
                omschrijving=omschrijving,
                email=email,
                GPS_locatie=Point(longitude, latitude),
                datum_melding=timezone.now(),
                status=status
            )

            # Save the Klacht object
            klacht.save()

            # Log the submitted data for debugging
            print(f"Submitted Klacht: Naam={naam}, Omschrijving={omschrijving}, Email={email}, Longitude={longitude}, Latitude={latitude}")

            return JsonResponse({'message': 'Klacht submitted successfully!'}, status=201)

        return JsonResponse({'error': 'Longitude and latitude are required'}, status=400)

    # Handle GET request or other cases
    return JsonResponse({'error': 'Method not allowed'}, status=405)
