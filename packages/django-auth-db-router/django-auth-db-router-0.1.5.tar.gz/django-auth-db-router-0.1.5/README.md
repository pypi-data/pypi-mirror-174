# Django auth DB router.

Simple database router that helps to split your main database and authentication database.
This may be necessary, for example, when splitting a project into microservices.

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
   
3. Add `auth_db` section to `DATABASES`:
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

4. Finally, add `AUTH_DB` setting:
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
   
   AUTH_DB = 'auth_db'
   ```
   
   Without this setting router will use `default` db connection.