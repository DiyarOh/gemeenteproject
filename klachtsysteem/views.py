from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .utils import is_valid_invitation_code 
from .models import Invitation

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def register_view(request, invitation_code=None):
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
    return render(request, 'invalid_code.html')


class ComplaintsFormView(TemplateView):
    template_name = "klachtenformulier.html"

class HomePageView(TemplateView):
    template_name = "homepage.html"
