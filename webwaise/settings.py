"""
Django settings for webwaise project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l#=l*t9j(p)m07t=p2art2&v0)vw2^xmd7!&#gzmlejt&tdky='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.environ.get('DEBUG') else True 

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'core.apps.CoreConfig',
    "corsheaders",
    
]


CSRF_TRUSTED_ORIGINS = ['https://webwaise.com',
                        'http://139.59.171.152',
                        'https://139.59.171.152',
                        'http://webwaise.com']

CORS_ALLOWED_ORIGINS = ['https://webwaise.com',
                        'http://139.59.171.152',
                        'https://139.59.171.152',
                        'http://webwaise.com']
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'webwaise.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'webwaise.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB','webwaise'),
        'USER': os.environ.get('POSTGRES_USER','webwaise'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD','webwaisellc2023!girenesoyusvar'),
        'HOST': os.environ.get('POSTGRES_HOST','localhost'),
        'PORT': os.environ.get('POSTGRES_PORT','5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True   


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STRIPE_PUBLIC_KEY = 'pk_test_51MT1tpIpI2DRrDdebyv7P50yM9p23WsKWaoDLsKMVXrybwa1lIcscDDP6ThKeNnAmldGqCkbzR6KQNKgFiwGfwcm00b13Ug8HD'
STRIPE_SECRET_KEY = 'sk_test_51MT1tpIpI2DRrDde4li8UJBGaNS73zugCRBzco8SHT71xKHy2byY41Aogmnt33dEbAJDWqTAfPs5d5MVTNsCBTcH00Xfdxda1D'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'trustact.business@gmail.com'
EMAIL_HOST_PASSWORD = 'htxrlvhcqabdenmy'
# esil parol multikartllc00


AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '211835480808-r6o3750p6uecc5knhctvambagu2k1dbs.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'



from django.urls import reverse_lazy
 
LOGIN_URL = reverse_lazy('core:signin')
LOGIN_REDIRECT_URL = reverse_lazy('core:home')
SOCIAL_AUTH_LOGIN_REDIRECT_URL = reverse_lazy('core:home')
LOGOUT_REDIRECT_URL = reverse_lazy('core:home')
LOGOUT_URL = reverse_lazy('core:logout')
