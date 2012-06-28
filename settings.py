# Django settings for expotaciones project.
import os.path

try:
    from local_settings import SITE_PREFIX, BASE_PATH
except:
    SITE_PREFIX = '/'
    BASE_PATH = '/opt/aplicaciones/'

APP_NAME = "imgdb"
DEBUG = True #False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('noname', 'test@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imgdb',
        'USER': 'imgdb',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

TIME_ZONE = 'America/Argentina/Buenos_Aires'
LANGUAGE_CODE = 'es-AR'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(BASE_PATH, 'media/')
MEDIA_URL = '%s/media/' % SITE_PREFIX
STATIC_ROOT = os.path.join(BASE_PATH, 'static/')
STATIC_URL = '%s/static/' % SITE_PREFIX
STATICFILES_DIRS = (
    ("basestatic"),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
SECRET_KEY = '8m*qy!*9su(*%xlk557fz$%10(7fsq8hq6v9sdw-+cb_#s=_hf'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)
ROOT_URLCONF = 'imgdb.urls'

TEMPLATE_DIRS = (os.path.join(BASE_PATH,'templates'),)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'main',
    'main.plugins',
)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
LOGIN_URL = '%s/login' % SITE_PREFIX
LOGIN_REDIRECT_URL = '%s/' % SITE_PREFIX

ITEMS_PER_PAGE = 10

try:
    from local_settings import *
except:
    pass
