# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.contrib.gis.db import models as geomodels

# Custom manager for Invitation model
class InvitationManager(models.Manager):
    def create_random_invitation(self):
        # Generate a random code for a new invitation
        code = get_random_string(length=20)
        return self.create(code=code)

# Invitation model
class Invitation(models.Model):
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_used = models.BooleanField(default=False)

    objects = InvitationManager()

    def save(self, *args, **kwargs):
        # Generate a random unique code if not provided
        if not self.code:
            self.code = get_random_string(length=20)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code if self.code else 'No Code'

# Status model
class Status(models.Model):
    waarde = models.CharField(max_length=255, null=False)  # Status value
    beschrijving = models.TextField()

    @classmethod
    def seed_status_data(cls):
        # Define a list of basic statuses
        status_data = [
            {'waarde': 'Open', 'beschrijving': 'The complaint is open and not yet resolved.'},
            {'waarde': 'In Progress', 'beschrijving': 'The complaint is currently being addressed.'},
            {'waarde': 'Closed', 'beschrijving': 'The complaint has been resolved and closed.'},
        ]

        # Create status objects if they don't already exist
        for status_info in status_data:
            status, created = cls.objects.get_or_create(
                waarde=status_info['waarde'],
                beschrijving=status_info['beschrijving']
            )

            if created:
                print(f"Created status: {status}")

    def __str__(self):
        return self.waarde

# Klacht model
class Klacht(models.Model):
    naam = models.CharField(max_length=50, null=False)
    omschrijving = models.CharField(max_length=300, null=False)
    email = models.EmailField(null=False)
    GPS_locatie = geomodels.PointField()  # GeoDjango specific field for storing geographic location
    datum_melding = models.DateTimeField(null=False)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, default=1) 

# Afbeelding model
class Afbeelding(models.Model):
    klacht = models.ForeignKey(Klacht, related_name='afbeeldingen', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='afbeeldingen/')
