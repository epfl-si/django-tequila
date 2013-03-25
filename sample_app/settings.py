# Django settings for sample_app project.
import os
this_dir = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.normpath(os.path.join(this_dir, 'database.db')),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '_jnlqznqi)s#h#=-v#faq_25^m_9+gjk8l^qmwjl6^iu)rztdf'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_tequila.middleware.TequilaMiddleware',
)

ROOT_URLCONF = 'sample_app.urls'

WSGI_APPLICATION = 'sample_app.wsgi.application'

TEMPLATE_DIRS = (
   os.path.normpath(os.path.join(this_dir, "templates")),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_tequila',
    'sample_app',    
)


AUTHENTICATION_BACKENDS = ('django_tequila.django_backend.TequilaBackend',)
AUTH_PROFILE_MODULE = "sample_app.userprofile"
TEQUILA_SERVICE_NAME = "django_tequila_service"
TEQUILA_SERVER_URL = "https://tequila.epfl.ch"
TEQUILA_NEW_USER_INACTIVE = False
TEQUILA_CLEAN_URL = True
TEQUILA_STRONG_AUTHENTICATION = True
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"
LOGIN_REDIRECT_IF_NOT_ALLOWED = "/not_allowed"
LOGOUT_URL = "/"