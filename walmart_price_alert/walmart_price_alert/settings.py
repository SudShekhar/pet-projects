"""
Django settings for walmart_price_alert project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_PATH = os.path.join(BASE_DIR, "templates")
REGISTRATION_OPEN =True
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e(@4c+=%xy#27%99u9wtipf$2c=$^&ts_+e&@$k#kgk-$pybl)'

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
    'wali',
    'django_social_share',
    'registration',
    'django_cron'
)

CRON_CLASSES = [
			'wali.cron.RollbackFeedsCronJob',
			'wali.cron.SpecialBuyFeedsCronJob',
			'wali.cron.ValuedayFeedsCronJob',
			'wali.cron.ValuehourFeedsCronJob',
			'wali.cron.ClearanceFeedsCronJob',
                        'wali.cron.ManageDiscountsCron'
		]
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'walmart_price_alert.urls'

WSGI_APPLICATION = 'walmart_price_alert.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
		'OPTIONS':{
			'read_default_file' : os.path.join(BASE_DIR, 'mycnf.cnf')
		},
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'walmartrequests@gmail.com'
EMAIL_HOST_PASSWORD = '********'
USE_TZ = True
TEMPLATE_CONTEXT_PROCESSORS = [
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.request"
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_DIRS = [
		os.path.join(BASE_DIR, "static")
]	
		
TEMPLATE_DIRS = (
		TEMPLATE_PATH,
		)
STATIC_URL = '/static/'
