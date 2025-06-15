# users/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# This gets the currently active user model from settings.py (AUTH_USER_MODEL)
# It's the correct, robust way to reference the User model.
User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Username'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}
    ))


class MinimalistUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Now this correctly points to whatever model is defined in settings.py
        model = User
        fields = ("username", "email")

    # Override the fields to remove help_text and add custom placeholders/widgets
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Choose a unique username'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'your.email@example.com'})
    )
    # The password fields from the parent UserCreationForm will be used,
    # and we style them manually in the template for consistency.