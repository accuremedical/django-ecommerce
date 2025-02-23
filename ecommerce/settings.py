"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import pymysql 
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / "templates"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-iz2+^p*@e#kih882t4v@f+cc3n_f@k2^xy8%komc3@bav9dd7_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_countries',
    'core',
    'accounts',
    

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMP_DIR],
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_db',
        'USER':'root',
        'PASSWORD':'Accumart@321',
        'HOST':'localhost',
        'PORT':'3306',
    }
}

'''
DATABASES = { 
    'default': {
         'ENGINE': 'django.db.backends.sqlite3', 
         'NAME': BASE_DIR / "db.sqlite3", 
         }
         }
'''

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",

]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

CSRF_COOKIE_SECURE = True

'''

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtpout.secureserver.net' 
EMAIL_PORT = 587  
EMAIL_USE_TLS = True 
EMAIL_HOST_USER = 'support@accuremedical.in' 
EMAIL_HOST_PASSWORD = 'Support@2023'  
DEFAULT_FROM_EMAIL = 'support@accuremedical.in'
ADMIN_EMAIL ='reenu@accuremedical.in'

'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587 
EMAIL_USE_TLS = True 
EMAIL_HOST_USER = 'accuremedicalpvtltd@gmail.com'
EMAIL_HOST_PASSWORD = 'tynv aaup qmeu rnzm'  
DEFAULT_FROM_EMAIL = 'accuremedicalpvtltd@gmail.com'  
ADMIN_EMAIL ='arhurai@gmail.com'




# razorpay payment gateway integration
RAZORPAY_ID ="rzp_test_EPAE67LdMYkVDm"
RAZORPAY_SECRET="IPxBQi0NYhQJ03M6hiOZGPDO"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# PAYU_MERCHANT_KEY = 'Rs1pDx'
# PAYU_MERCHANT_SALT = 'Ynv7qKmRzqoU0zzK2578OILBHa5Sb7CJ'
# PAYU_MERCHANT_ID = 'de5245e71c0854a5988917bfd99c7c22910e902f10a2883879362bf9d8099e38'
# PAYU_API_URL = 'https://secure.payu.in/_payment'  # Use the appropriate URL (test or live)

PAYU_MERCHANT_KEY_TEST = '8A6lU0'
PAYU_MERCHANT_SALT_TEST = '6WM5jhuuCISJmxYnyHhjOB74kfTT2aki'
PAYU_MERCHANT_ID_TEST = 'a7b8391d5300960d1af5d1e6c59ddecb3c14437efe3acbcdcb617abdbe1cb28e'
PAYU_API_URL_TEST = 'https://test.payu.in/_payment'


# PayU success and failure URLs for local development
PAYU_SUCCESS_URL = 'http://localhost:8000/payment_success'  
PAYU_FAILURE_URL = 'http://localhost:8000/payment_failure'
