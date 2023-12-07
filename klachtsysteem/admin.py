from django.contrib import admin
from .models import Invitation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used')
    search_fields = ('code',)