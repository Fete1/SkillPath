from django.contrib import admin
from django.urls import path, include
from core.views import HomePageView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # Import auth_views
from users.forms import CustomAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    
    # Add accounts urls for login/logout
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),  # Our sign up url
    path('tours/', include('tours.urls')),
    path('', HomePageView.as_view(), name='home'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('booking/', include('bookings.urls')),
    path('blog/', include('blog.urls')),
    path('reviews/', include('reviews.urls')),
    path('affiliates/', include('affiliates.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)