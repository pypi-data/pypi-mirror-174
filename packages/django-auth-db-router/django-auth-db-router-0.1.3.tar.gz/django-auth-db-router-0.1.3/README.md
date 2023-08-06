# Simple database router.

Simple database router was originally written for personal and work purposes.

## Quickstart

1. Add `django_auth_db_router` to your `INSTALLED_APPS` setting like this:
    ```
    INSTALLED_APPS = [
        ...
        'django_auth_db_router',
        ...
    ]
    ```

2. Add `DATABASE_ROUTERS` setting in `settings.py` file:
    ```
    DATABASE_ROUTERS = [
        'django_auth_db_router.routers.AuthRouter',
    ]
    ```

3. Finally, add `auth_db` section to `DATABASES`:
   ```
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'default.sqlite3',
       },
       'auth_db': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'auth.sqlite3',
       },
   }
    ```