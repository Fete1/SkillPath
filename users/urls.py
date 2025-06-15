# users/urls.py
from django.urls import path
from .views import SignUpView, dashboard # Import the dashboard view

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('dashboard/', dashboard, name='dashboard'), # Add this line
]