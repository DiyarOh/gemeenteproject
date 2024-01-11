from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .utils import is_valid_invitation_code 
from .models import Invitation, Klacht, Status
from .forms import ComplaintSearchForm

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        # If the user is logged in, redirect them to the home page
        return redirect('complaints_dashboard') 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('complaints_dashboard')
        else:
            return render(request, 'login.html', {'errors': ['Invalid credentials']})

    return render(request, 'login.html')


def register_view(request, invitation_code=None):
    if request.user.is_authenticated:
        # If the user is logged in, redirect them to the home page
        return redirect('complaints_dashboard') 

    # Check if the invitation code is valid
    if invitation_code is None or not is_valid_invitation_code(invitation_code) or invitation_code == '':
        return redirect('invalid_code')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Mark the invitation code as used
            invitation = Invitation.objects.get(code=invitation_code)
            invitation.is_used = True
            invitation.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form, 'invitation_code': invitation_code})

def invalid_code_view(request):
    if request.user.is_authenticated:
        # If the user is logged in, redirect them to the home page
        return redirect('complaints_dashboard') 
    return render(request, 'invalid_code.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class ComplaintsFormView(TemplateView):
    template_name = "klachtenformulier.html"

class HomePageView(TemplateView):
    template_name = "homepage.html"


class ComplaintsDashboard(ListView):
    model = Klacht
    template_name = 'klachtbeheer.html'
    context_object_name = 'klachten'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        search_desc = self.request.GET.get('search_desc')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')

        queryset = Klacht.objects.all()
        # Order the queryset by the 'datum_melding' field
        queryset = queryset.order_by('datum_melding')

        if search_query:
            # Search title/naam
            queryset = queryset.filter(naam__icontains=search_query)

        if search_desc:
            # Search description/omschrijving 
            queryset = queryset.filter(omschrijving__icontains=search_desc)

        if start_date:
            # Convert start_date string to a datetime object
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            queryset = queryset.filter(datum_melding__gte=start_date)

        if end_date:
            # Convert end_date string to a datetime object
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            queryset = queryset.filter(datum_melding__lte=end_date)

        if status:
            # Search status
            queryset = queryset.filter(status__id=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ComplaintsDashboard, self).get_context_data(**kwargs)
        
        # Get the filtered queryset
        filtered_queryset = self.get_queryset()
        
        # Set up pagination
        paginator = Paginator(filtered_queryset, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            klachten = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            klachten = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            klachten = paginator.page(paginator.num_pages)

        # Update context with the paginated queryset
        context[self.context_object_name] = klachten
        context['search_form'] = ComplaintSearchForm(self.request.GET)
        context['statuses'] = Status.objects.all()

        return context