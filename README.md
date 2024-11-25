# Django SaaS Demo

## Setup
```
python -m venv
source venv/bin/activate
pip install -r requirements.txt
```

### migrate
```
cd src
python manage.py makemigrations
python manage.py migrate
```

### download css, js cdn to local
```
python manage.py assets_pull
python manage.py collectstatic # download css, js cdn to local
```

### run server
```
python manage.py runserver
Access link http://127.0.0.1:8000/
```

### Create SECRET_KEY
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
openssl rand -base64 32
```


### some errors
https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org

## Links
```
https://docs.allauth.org/en/latest/index.html
https://github.com/pennersr/django-allauth
https://github.com/danihodovic/django-allauth-ui

https://railway.app/
https://neon.tech/(PostgreSQL)
```