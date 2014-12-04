mondroid
========

Simple monitoring system written in Python/Django using requests.

install
========

Clone repo and create database

Update/create settings.py based on dev or test settings files provided.

If you are using virtualenv, create a new environment and from the root directory run:

```
pip install -r requirements.txt
```

Then from the src folder run:

```
python manage.py syncdb
```

Follow by

```
python manage.py collectstatic
```

Done.
