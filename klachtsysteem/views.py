from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
        return redirect('home') 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'errors': ['Invalid credentials']})

    return render(request, 'login.html')


def register_view(request, invitation_code=None):
    if request.user.is_authenticated:
        # If the user is logged in, redirect them to the home page
        return redirect('home') 

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
        return redirect('home') 
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
    paginate_by = 10
    ordering = ['-datum_melding']

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')

        queryset = Klacht.objects.all()

        if search_query:
            queryset = queryset.filter(naam__icontains=search_query)

        if start_date:
            queryset = queryset.filter(datum_melding__gte=start_date)

        if end_date:
            queryset = queryset.filter(datum_melding__lte=end_date)

        if status:
            queryset = queryset.filter(status__id=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ComplaintSearchForm(self.request.GET)
        context['statuses'] = Status.objects.all()  # Provide status choices to the template
        return context