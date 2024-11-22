# Django SaaS Demo

## Setup

### Create SECRET_KEY
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
openssl rand -base64 32
```


### generate assets static file
```
python manage.py collectstatic
```