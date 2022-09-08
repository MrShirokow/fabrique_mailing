from .settings import *

DATABASES = {
    'default': {
        'ENGINE': env('POSTGRES_ENGINE'),
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': env('POSTGRES_PORT')
    }
}
