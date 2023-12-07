from django.db import models
from django.utils.crypto import get_random_string

class InvitationManager(models.Manager):
    def create_random_invitation(self):
        code = get_random_string(length=20)
        return self.create(code=code)

class Invitation(models.Model):
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate a random unique code if not provided
        if not self.code:
            self.code = get_random_string(length=20)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code if self.code else 'No Code'