from django import forms
from .models import Status


class ComplaintSearchForm(forms.Form):
    search_query = forms.CharField(
        label='Zoek Melder',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Voeg naam toe'}),
    )
    start_date = forms.DateField(label='Start Datum', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Datum', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label='Status',
        required=False,
        empty_label='Any Status',
    )