from pathlib import Path
import os
import dj_database_url

# ---------------- Base Directory ----------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- Security ----------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "replace-with-your-own-secret-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# ---------------- Allowed Hosts ----------------
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost 127.0.0.1").split()
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split()

# ---------------- Installed Apps ----------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',  # Your app
]

# ---------------- Middleware ----------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------- URL Configuration ----------------
ROOT_URLCONF = 'smartclass_project.urls'

# ---------------- Templates ----------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  
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

# ---------------- WSGI ----------------
WSGI_APPLICATION = 'smartclass_project.wsgi.application'

# ---------------- Database ----------------
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

# ---------------- Password Validators ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- Authentication ----------------
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
LOGIN_REDIRECT_URL = '/'   
LOGOUT_REDIRECT_URL = '/'  
LOGIN_URL = '/accounts/login/'

# ---------------- Internationalization ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
USE_L10N = True

# ---------------- Static Files ----------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'users' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------- Media Files ----------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------- Email ----------------
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)

# ---------------- Default Auto Field ----------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
