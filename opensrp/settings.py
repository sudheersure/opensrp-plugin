"""
Django settings for opensrp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7lx599_c*gwws^)!jncu1^ir4!=ufxxttudwj09ztdey(gx=xp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Masters',
    'multiselectfield',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'opensrp.urls'

WSGI_APPLICATION = 'opensrp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'opensrp',
        'USER': 'dhanush',
        'PASSWORD': 'dhanush',
        'HOST': '10.10.11.79',
        'PORT': '5432',
        'OPTIONS': {
           'options': '-c search_path=report'
        }
    },
 'dynamic_data':{
   'ENGINE': 'django.db.backends.sqlite3',
   'NAME':'test',
   'USER':'',
   'PASSWORD':''
 },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
# STATIC_ ROOT= '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
DRUG_MAP = {"CHILD":0,"PNC":1,"ANC":2}
USER_ROLE={"ANM":"ROLE_USER","PHC":"ROLE_PHC_USER","DOC":"ROLE_DOC_USER"}
STATICFILES_DIRS = (BASE_DIR + '/static',)


import sys
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }

DISEASES = ('Pallor',
'Swelling / Edema',
'Bleeding',
'Jaundice',
'Fits / Convulsions',
'Difficult Breathing',
'Bad Headache',
'Blurred Vision',
'Uterus is soft or tender',
'Abdominal Pain',
'Bad Smelling lochea',
'Heavy Bleeding per vaginum',
'Infected perineum suture',
'Difficulty Passing Urine',
'Burning sensation when urinating',
'Breast Hardness',
'Nipple Hardness',
'Mealses',
'Diarrhea and dehydration',
'Malaria',
'Acute Respiratory Infection',
'Severe Acute Mal Nutrition',
'Cough',
'Diarrhea',
'Fever',
'Convulsions',
'Vomiting')


PHONE_NUMBER_LENGTH = 10