# affiliates/models.py
import uuid
from django.db import models
from django.conf import settings

class Affiliate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # The unique code the affiliate will use in their links
    affiliate_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username