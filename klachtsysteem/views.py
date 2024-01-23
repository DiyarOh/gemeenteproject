# views.py
import json

from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .utils import is_valid_invitation_code 
from .models import Invitation, Klacht, Status
from .forms import ComplaintSearchForm, KlachtForm, KlachtStatusForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as geomodels
from django.http import JsonResponse
from django.utils import timezone
from django.core.serializers import serialize
from django.utils.dateformat import DateFormat
from django.urls import reverse_lazy


# Make sure to import Status model
from .models import Klacht, Status, Afbeelding

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


def serialize_klachten(klachten):
    # This function will manually serialize the Klacht data and format the dates
    return json.dumps([
        {
            'id': klacht.id,  # Include the ID
            'naam': klacht.naam,
            'omschrijving': klacht.omschrijving,
            'GPS_locatie': {'lat': klacht.GPS_locatie.y, 'lng': klacht.GPS_locatie.x},
            'datum_melding': DateFormat(klacht.datum_melding).format('c')  # ISO 8601 format
        }
        for klacht in klachten
    ])

# Complaints form view
class ComplaintsFormView(TemplateView):
    template_name = "klachtformulier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = KlachtForm()  # Add the form to the context
        return context
    
    def post(self, request):
        print(request.FILES)
        form = KlachtForm(request.POST, request.FILES)
        if form.is_valid():
            # Retrieve form data using cleaned_data
            naam = form.cleaned_data['naam']
            omschrijving = form.cleaned_data['omschrijving']
            email = form.cleaned_data['email']
            longitude = form.cleaned_data['longitude'] 
            latitude = form.cleaned_data['latitude'] 
            foto = form.cleaned_data['foto']

            # Get or create the Status object with ID 1
            status, created = Status.objects.get_or_create(id=1, defaults={'waarde': 'Default', 'beschrijving': 'Default status'})

            # Create Klacht object
            klacht = Klacht(
                naam=naam,
                omschrijving=omschrijving,
                email=email,
                GPS_locatie=Point(float(longitude), float(latitude)),
                datum_melding=timezone.now(),
                status=status
            )

            try:
                # Save the Klacht object
                klacht.save()
                print(foto)

                # Save uploaded files to the DB
                if foto:
                    afbeelding = Afbeelding(klacht=klacht)
                    afbeelding.image_file = foto
                    afbeelding.save()

                return render(request, self.template_name, {'message': 'Klacht submitted successfully!', 'form': form})
            except Exception as e:
                return render(request, self.template_name, {'error': f"An error occurred: {e}"})
        else:
            # Form is not valid, return the form with errors
            return render(request, self.template_name, {'form': form})


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
        klacht_id = self.request.GET.get('id')

        # Retrieve all complaints and order by submission date
        queryset = Klacht.objects.all()
        queryset = queryset.order_by('-datum_melding')

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
        
        if klacht_id:
            queryset = queryset.filter(id=klacht_id)

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

        # Check for klachten older than 2 weeks
        two_weeks_ago = timezone.now() - timezone.timedelta(weeks=2)
        old_klachten = filtered_queryset.filter(datum_melding__lt=two_weeks_ago)
        
        # Prepare context data
        context = super(ComplaintsDashboard, self).get_context_data(**kwargs)
        context[self.context_object_name] = klachten
        context['search_form'] = ComplaintSearchForm(self.request.GET)
        context['statuses'] = Status.objects.all()

        # Add a notification if there are old klachten
        if old_klachten.exists():
            context['old_klachten_notification'] = f"There are {old_klachten.count()} klachten older than 2 weeks."

        return context

class KlachtMapView(TemplateView):
    template_name = 'klachtmap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve all Klacht objects from the database
        klachten = Klacht.objects.all()

        # Add the serialized data to the context
        context['klachten_json'] = serialize_klachten(klachten)

        return context
    

class KlachtDetailView(DetailView, UpdateView):
    model = Klacht
    template_name = 'klacht.html'  # specify your template name
    form_class = KlachtStatusForm
    context_object_name = 'klacht'

    def get_success_url(self):
        return reverse_lazy('klacht', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['afbeeldingen'] = self.object.afbeeldingen.all()  # Add the related images to the context
        return context
    

class KlachtDeleteView(DeleteView):
    model = Klacht
    success_url = reverse_lazy('complaints_dashboard') 