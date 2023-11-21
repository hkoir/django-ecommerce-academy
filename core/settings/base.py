import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = "3xk*)i0x#k$btl=(6q)te!19=mp6d)lm1+zl#ts4ewxi3-!vm_"
SITE_ID = 1
DEBUG = True

ALLOWED_HOSTS = ["yourdomain.com", "127.0.0.1", "localhost","192.168.0.106"]

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
    "basket",
    "account",
    "orders",
    "mptt",
    "core",
    'vendors',
    'seller',
     'django.contrib.sites',
    'django.contrib.sitemaps',
    'companyprofile'
  
   
]

MIDDLEWARE = [
  
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
     'django.contrib.sites.middleware.CurrentSiteMiddleware',
    
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.context_processors.categories",
                "basket.context_processors.basket",
                "account.context_processors.user_info",
                # "store.context_processors.product_stars",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")



#......................Amazon s3 bucket setting..........................................
# AWS_ACCESS_KEY_ID = 'AKIA36PKXMOZQLJE2IP2'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = 'ddealshop'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_DEFAULT_ACL = None

# AWS_S3_SIGNATURE_NAME = 's3v4',
# AWS_S3_REGION_NAME = 'ap-southeast-1'
# AWS_S3_FILE_OVERWRITE = False
# AWS_S3_VERITY = True

# AWS_LOCATION = 'static'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'core.storages.MediaStore'

# MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, 'media')  # Adjust the URL path
# MEDIA_ROOT = '/media/'
#.............................................Amazon end .............................................

# Basket session ID
BASKET_SESSION_ID = "basket"

# Stripe Payment
os.environ.setdefault(
    "STRIPE_PUBLISHABLE_KEY",
    "pk_test_51IHxTTJm9Ogh6om63DrCDlFfxcPDTvbUVy1CoSiI1ZS2GKt8UJojUJlbo9CAOCHnNgEqwKlQlnv9TmyzKIUUkr8800w8nNvBfw",
)
STRIPE_SECRET_KEY = (
    "sk_test_51IHxTTJm9Ogh6om6ryBhjePFWUTXvweI5y5gXjFhgPWVztF83X6Rhae1LGfW8bteV5ebb2KhX9w61Q1117Sw1iHE00gzR7PmNq"
)
# stripe listen --forward-to localhost:8000/payment/webhook/

# Custom user model
AUTH_USER_MODEL = "account.Customer"
LOGIN_REDIRECT_URL = "/account/dashboard"
LOGIN_URL = "/account/login/"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"// this will shows notification in console.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  # or 587 for TLS
EMAIL_USE_SSL = True  # Use SSL for secure connection
EMAIL_HOST_USER = 'mycpa1973@gmail.com'
EMAIL_HOST_PASSWORD = 'jkpktzdmffwvkrdh'
DEFAULT_FROM_EMAIL = 'mycpa1973@gmail.com' 






