from django.contrib import admin
from .models import Invitation, Status, Klacht, Afbeelding

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used')
    search_fields = ('code',)

# Define the admin class for the Status model
class StatusAdmin(admin.ModelAdmin):
    list_display = ['waarde', 'beschrijving']

# Register the Status model with its admin class
admin.site.register(Status, StatusAdmin)

# Define the admin class for the Klacht model
class KlachtAdmin(admin.ModelAdmin):
    list_display = ['naam', 'omschrijving', 'email', 'datum_melding', 'status']
    list_filter = ['status']
    search_fields = ['naam', 'email']
    date_hierarchy = 'datum_melding'

# Register the Klacht model with its admin class
admin.site.register(Klacht, KlachtAdmin)

# Define the admin class for the Afbeelding model
class AfbeeldingAdmin(admin.ModelAdmin):
    list_display = ['klacht', 'image_file']

# Register the Afbeelding model with its admin class
admin.site.register(Afbeelding, AfbeeldingAdmin)