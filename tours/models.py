# tours/models.py
from django.db import models
from django.utils.text import slugify
from django.db.models import Avg, Count

class Destination(models.Model):
    name = models.CharField(max_length=100)
    # A 'slug' is a URL-friendly version of the name, e.g., "new-york-city"
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='cities')
    image = models.ImageField(upload_to='cities/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.destination.name}"

class Tour(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='tours')
    description = models.TextField()
    # Use DecimalField for money to avoid floating point errors
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    max_guests = models.PositiveIntegerField(default=15)
    def review_count(self):
        # We only want to count APPROVED reviews.
        return self.reviews.filter(is_approved=True).aggregate(Count('id'))['id__count']
    
    def average_rating(self):
        # We only want to average APPROVED reviews.
        return self.reviews.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg'] or 0
       

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name