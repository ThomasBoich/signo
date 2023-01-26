
DEBUG = False

ALLOWED_HOSTS =  ['95.163.233.127', 'sign-o.ru', 'www.sign-o.ru']

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

STATIC_URL = 'https://static.sign-o.ru/static/'
MEDIA_URL = 'https://static.sign-o.ru/media/'

MEDIA_ROOT = '/home/media_files'
STATIC_ROOT = '/home/static_files'



CSRF_TRUSTED_ORIGINS = ['http://95.163.233.127', 'http://sign-o.ru', 'https://sign-o']

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

