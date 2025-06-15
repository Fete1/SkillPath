# accounts/models.py
from django.db import models
from django.conf import settings
from affiliates.models import Affiliate

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # This field will store which affiliate referred the user.
    referred_by = models.ForeignKey(Affiliate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"