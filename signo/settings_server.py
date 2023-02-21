
DEBUG = False

ALLOWED_HOSTS =  ['194.67.106.188', 'sign-o.ru', 'www.sign-o.ru']

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

STATIC_URL = 'https://static.sign-o.ru/static/'
MEDIA_URL = 'https://static.sign-o.ru/media/'

MEDIA_ROOT = '/opt/django/media_files'
STATIC_ROOT = '/opt/django/static_files'



CSRF_TRUSTED_ORIGINS = ['http://194.67.106.188', 'http://sign-o.ru', 'https://sign-o.ru']

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '1234Rtyu',
        'HOST': 'db',
        'PORT': '5432',
    }
}

