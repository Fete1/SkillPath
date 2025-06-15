# reviews/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from tours.models import Tour

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    is_approved = models.BooleanField(default=False) # Admins must approve reviews
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only write one review per tour
        unique_together = ('tour', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.tour.name}"