import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv







from django.db.models.signals import post_migrate

def force_sync_database_tables(sender, **kwargs):
    from django.core.management import call_command
    print("🚀 Triggering deep database table auto-generation routine...")
    try:
        call_command('makemigrations', 'myapp', interactive=False)
        call_command('migrate', 'myapp', interactive=False)
    except Exception as e:
        print(f"⚠️ Initialization bypass notice: {e}")

# This hooks into Django's startup sequence and executes the build commands automatically
if 'runserver' in sys.argv or 'gunicorn' in sys.argv or 'uvicorn' in sys.argv or 'wsgi' in sys.argv:
    post_migrate.connect(force_sync_database_tables)



# =====================================================================
# EMERGENCY DATABASE FORCE-SYNC (BROWSER-ONLY CONFIGURATION)
# =====================================================================
import os
from django.db import connection

def execute_immediate_table_sync():
    """
    Executes immediately when settings.py compiles on Render.
    Talks directly to Postgres to map the missing tables.
    """
    print("🚀 Running immediate raw database table creation sequence...")
    
    # Simple sanity safety wrapper
    with connection.cursor() as cursor:
        try:
            # 1. Inject the core Product model structure 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "myapp_product" (
                    "id" bigserial NOT NULL PRIMARY KEY,
                    "title" varchar(255) NOT NULL,
                    "description" text NOT NULL,
                    "price" numeric(12, 2) NOT NULL,
                    "condition" varchar(10) NOT NULL,
                    "stock_count" integer NOT NULL CHECK ("stock_count" >= 0),
                    "item_location" varchar(10) NOT NULL,
                    "seller_location_details" varchar(255) NOT NULL,
                    "created_at" timestamptz NOT NULL,
                    "seller_id" integer NOT NULL
                );
            """)
            
            # 2. Attach the User profile link constraint index safely
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.table_constraints 
                        WHERE constraint_name = 'myapp_product_seller_id_fk_auth_user_id'
                    ) THEN
                        ALTER TABLE "myapp_product" 
                        ADD CONSTRAINT "myapp_product_seller_id_fk_auth_user_id" 
                        FOREIGN KEY ("seller_id") REFERENCES "auth_user" ("id") 
                        DEFERRABLE INITIALLY DEFERRED;
                    END IF;
                END $$;
            """)
            
            # 3. Inject the Photo storage model table structure
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "myapp_photo" (
                    "id" bigserial NOT NULL PRIMARY KEY,
                    "image" varchar(255) NOT NULL,
                    "created_at" timestamptz NOT NULL,
                    "product_id" bigint NULL
                );
            """)
            
            # 4. Attach the Photo to Product relationship link index
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.table_constraints 
                        WHERE constraint_name = 'myapp_photo_product_id_fk_myapp_product_id'
                    ) THEN
                        ALTER TABLE "myapp_photo" 
                        ADD CONSTRAINT "myapp_photo_product_id_fk_myapp_product_id" 
                        FOREIGN KEY ("product_id") REFERENCES "myapp_product" ("id") 
                        DEFERRABLE INITIALLY DEFERRED;
                    END IF;
                END $$;
            """)
            print("======== ✅ DATABASE TABLES SUCCESSFULLY FORCED ON INIT ======== ")
        except Exception as e:
            print(f"⚠️ Table execution bypass or tracking notice: {e}")

# Run it immediately on application bootstrap
execute_immediate_table_sync()



load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-fallback-key-change-me")

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.getenv("DEBUG", "False") == "True"
DEBUG =True

ALLOWED_HOSTS = ["*"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Cloudinary Configuration
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    secure=True
)

# CLOUDINARY_STORAGE is still needed for the django-cloudinary-storage library,
# but it will automatically use the CLOUDINARY_URL if you leave it empty
# or remove the manual key/secret entries.
CLOUDINARY_STORAGE = {
    # If using CLOUDINARY_URL, you can leave this dictionary empty
    # or just include non-credential settings.
}




DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

INSTALLED_APPS = [
    'unfold', # 🌟 PLACED FIRST TO OVERRIDE THE ADMIN UI
    'unfold.contrib.filters', # Optional modern filter cards
    'cloudinary_storage',
    "django.contrib.admin",
    'cloudinary',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "myapp",
    "rest_framework",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "myproject.wsgi.application"

# Database Configuration (Supports Render DATABASE_URL automatically)
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & Media Files




DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# Static & Media Files Configuration
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Add these two lines to fix the crash:
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'


# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    # Add your live frontend Render URL here once deployed, e.g.:
    # "https://your-frontend-app.onrender.com"
]

CORS_ALLOW_CREDENTIALS = True
# If you want to allow all origins safely while supporting credentials or specific testing:
# CORS_ALLOW_ALL_ORIGINS = True


# Enables compression and aggressive caching for fast loading speeds
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
