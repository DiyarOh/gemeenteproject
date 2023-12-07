from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .utils import is_valid_invitation_code 

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('success')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def register_view(request, invitation_code=None):
    # Check if the invitation code is valid
    if invitation_code is None or not is_valid_invitation_code(invitation_code):
        return redirect('invalid_invitation')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Mark the invitation code as used
            invitation = Invitation.objects.get(code=invitation_code)
            invitation.is_used = True
            invitation.save()

            return redirect('success')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form, 'invitation_code': invitation_code})


class ComplaintsFormView(TemplateView):
    template_name = "klachtenformulier.html"

class HomePageView(TemplateView):
    template_name = "homepage.html"
