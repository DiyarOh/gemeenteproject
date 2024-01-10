from .models import Invitation

def is_valid_invitation_code(code):
    try:
        invitation = Invitation.objects.get(code=code, is_used=False)
        return True
    except Invitation.DoesNotExist:
        return False