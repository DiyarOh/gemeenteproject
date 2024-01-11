from django import forms
from .models import Status



class ComplaintSearchForm(forms.Form):
    search_query = forms.CharField(
        label='Search Complaints',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter keywords'}),
    )
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label='Status',
        required=False,
        empty_label='Any Status',
    )