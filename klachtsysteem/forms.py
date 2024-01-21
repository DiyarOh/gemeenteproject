from django import forms
from .models import Status
from django.forms.widgets import FileInput
from django.core.exceptions import ValidationError


class MultiFileInput(FileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None, *args, **kwargs):
        default_attrs = {'multiple': 'multiple'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, *args, **kwargs)


class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, data):
        if data in self.empty_values:
            return None
        elif not hasattr(data, 'multiple'):
            raise ValidationError(self.error_messages['invalid'])
        return data


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

class KlachtForm(forms.Form):
    naam = forms.CharField(label='Naam', max_length=100, required=True)
    omschrijving = forms.CharField(label='Omschrijving', widget=forms.Textarea, required=True)
    email = forms.EmailField(label='Email', required=True)
    foto = forms.ImageField(required=False)
    longitude = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'longitude'}), required=True)
    latitude = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'latitude'}), required=True)