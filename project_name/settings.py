import datetime
import os
from configurations import Configuration, values
from unipath import Path


class Base(Configuration):

    ROOT_DIR = Path(os.path.abspath(__file__)).ancestor(2)

    PROJECT_DIR = Path(os.path.abspath(__file__)).parent

    INSTALLED_APPS = [
        # Django contrib apps
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.humanize',
        'django.contrib.sites',
        'django.contrib.sitemaps',
        'django.contrib.redirects',
        'django.contrib.flatpages',

        # Third-party apps, patches, fixes
        'imagekit',
        'widget_tweaks',
        'ckeditor',
        'ckeditor_uploader',
        'pytils',
        'axes',
        'compressor',
        #'rest_framework',

        # Local apps, referenced via '{{ project_name }}.appname'
        '{{ project_name }}.accounts',

        'django.contrib.auth',
        'django.contrib.admin',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
        'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
        'axes.middleware.AxesMiddleware',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                PROJECT_DIR.child('templates'),
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['DJANGO_DATABASE_NAME'],
            'USER': os.environ['DJANGO_DATABASE_USER_NAME'],
            'PASSWORD': os.environ['DJANGO_DATABASE_PASSWORD'],
            'HOST': 'localhost',
            'PORT': '',
            'CONN_MAX_AGE': 600,
        }
    }

    ADMINS = (
        ('Alexey Grigoriev', 'grialexey@gmail.com'),
    )

    MANAGERS = ADMINS

    ROOT_URLCONF = '{{ project_name }}.urls'

    WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

    ALLOWED_HOSTS = values.ListValue()

    SECRET_KEY = values.Value()

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'Europe/Moscow'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    
    STATICFILES_DIRS = [PROJECT_DIR.child('static'), ]

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    )

    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

    LOGIN_REDIRECT_URL = '/'

    AUTH_USER_MODEL = 'accounts.CustomUser'

    AUTHENTICATION_BACKENDS = [
        'axes.backends.AxesBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]

    SITE_ID = 1

    EMAIL_USE_TLS = values.BooleanValue(True)
    EMAIL_HOST = values.Value()
    EMAIL_HOST_USER = values.EmailValue()
    EMAIL_PORT = values.IntegerValue()
    DEFAULT_FROM_EMAIL = values.Value()
    SERVER_EMAIL = values.Value()
    EMAIL_HOST_PASSWORD = values.Value()

    THUMBNAIL_SUBDIR = 'thumbs'

    CKEDITOR_UPLOAD_PATH = 'ckeditor_uploads/'
    CKEDITOR_IMAGE_BACKEND = 'pillow'
    CKEDITOR_CONFIGS = {
        'default': {
            'removePlugins': 'stylesheetparser',
            'allowedContent': True,
            'toolbar': [
                ['Undo', 'Redo'],
                ['Format', 'Font', 'FontSize'],
                ['Link', 'Unlink', 'Anchor'],
                ['Image', 'Table', 'HorizontalRule'],
                ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', ],
                ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
                ['TextColor', 'BGColor'],
                ['Audio', 'Video'],
                ['Smiley', 'SpecialChar'],
                ['Source'],
                ['Embed'],
                ['Iframe'],
                ['CodeSnippet'],
            ],
            'codeSnippet_theme': 'github',
            'extraPlugins': ','.join(
                [
                    # your extra plugins here
                    'div',
                    'autolink',
                    'autoembed',
                    'embedsemantic',
                    # 'autogrow',
                    # 'devtools',
                    'widget',
                    'lineutils',
                    'clipboard',
                    'dialog',
                    'embed',
                    'iframe',
                    'dialogui',
                    'elementspath',
                    'codesnippet',
                ]),
            'height': 1000,
            'width': 700,
        },
    }

    AXES_LOGIN_FAILURE_LIMIT = 5
    AXES_COOLOFF_TIME = datetime.timedelta(minutes=15)

    AXES_LOCKOUT_TEMPLATE = 'registration/locked.html'

    IPWARE_META_PRECEDENCE_ORDER = (
        'HTTP_X_REAL_IP',
    )


class Dev(Base):
    DEBUG = True

    PUBLIC_DIR = Base.ROOT_DIR.child('public')
    STATIC_ROOT = PUBLIC_DIR.child('static')
    MEDIA_ROOT = PUBLIC_DIR.child('media')

    INTERNAL_IPS = (
        '127.0.0.1',
        '10.0.2.2',
    )

    MIDDLEWARE = Base.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INSTALLED_APPS = Base.INSTALLED_APPS + [
        'debug_toolbar',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda x: False
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            # 'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            # 'LOCATION': '127.0.0.1:11211',
            # 'OPTIONS': {
            #     'server_max_value_length': 1024 * 1024 * 10,  # size limit 10MB
            # }
        }
    }

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


class Prod(Base):
    DEBUG = False

    PUBLIC_DIR = Base.ROOT_DIR.parent.child('public')
    STATIC_ROOT = PUBLIC_DIR.child('static')
    MEDIA_ROOT = PUBLIC_DIR.child('media')

    FILE_UPLOAD_PERMISSIONS = 0o644

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'OPTIONS': {
                'server_max_value_length': 1024 * 1024 * 10,  # size limit 10MB
            }
        }
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': Base.ROOT_DIR.parent.child('logs', 'django.error.log'),
                'formatter': 'verbose',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['file', 'mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
