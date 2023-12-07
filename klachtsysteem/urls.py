from django.urls import path
from .views import ComplaintsFormView, register_view


urlpatterns = [
    path('klachtenformulier/', ComplaintsFormView.as_view(), name='complaints_form'),
    path('register/<str:invitation_code>/', register_view, name='register_with_invitation'),

]
