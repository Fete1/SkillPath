"""
Django settings for travel_platform project.
Modified for deployment on Render.
"""
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import dj_database_url # <-- MODIFICATION: Import dj-database-url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Use an environment variable for the secret key.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-local-dev') # <-- MODIFICATION

# DEBUG mode is False in production, True in development.
# Render sets the 'RENDER' environment variable.
DEBUG = 'RENDER' not in os.environ # <-- MODIFICATION

# Allowed hosts will include your Render app's URL.
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME') # <-- MODIFICATION
if RENDER_EXTERNAL_HOSTNAME: # <-- MODIFICATION
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME) # <-- MODIFICATION


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # <-- MODIFICATION: Add WhiteNoise
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_bootstrap5',  # <-- CORRECTION: Use bootstrap5 pack for your templates
    'core.apps.CoreConfig',
    'tours.apps.ToursConfig',
    'users.apps.UsersConfig',
    'bookings.apps.BookingsConfig',
    'paypal.standard.ipn',
    'blog.apps.BlogConfig',
    'reviews.apps.ReviewsConfig',
    'promotions.apps.PromotionsConfig',
    'affiliates.apps.AffiliatesConfig',
    'accounts.apps.AccountsConfig',
    'support.apps.SupportConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- MODIFICATION: Add WhiteNoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'affiliates.middleware.AffiliateMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ... (LANGUAGES and LOCALE_PATHS are fine) ...

ROOT_URLCONF = 'travel_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'travel_platform.wsgi.application'

# Use bootstrap5 crispy forms pack to match your templates
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5" # <-- MODIFICATION
CRISPY_TEMPLATE_PACK = 'bootstrap5'      # <-- MODIFICATION

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Database
# Uses PostgreSQL in production (on Render) and SQLite locally.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
if 'RENDER' in os.environ: # <-- MODIFICATION: Production Database Config
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        ssl_require=True,
    )

# ... (Password validation is fine) ...

# ... (Internationalization is fine) ...

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Tell WhiteNoise to serve files from the staticfiles directory and handle compression/caching
STORAGES = { # <-- MODIFICATION
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# PayPal settings from environment variables
PAYPAL_TEST = os.environ.get('PAYPAL_TEST') == 'True' # <-- MODIFICATION
PAYPAL_RECEIVER_EMAIL = os.environ.get('PAYPAL_RECEIVER_EMAIL') # <-- MODIFICATION
