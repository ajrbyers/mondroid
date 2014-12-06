# mondroid

Simple monitoring system written in Python/Django using requests.

## installation

Clone repo:

	$ git clone https://github.com/ajrbyers/mondroid.git

If you use [virtualenv](https://virtualenvwrapper.readthedocs.org/en/latest/), 
create a new virtualenv and switch to it.

Install requirements:

	$ sudo apt-get install sqlite3
	$ pip install -r requirements.txt

Make your own settings file:

	$ cp src/core/dev_settings.py src/core/settings.py

Create a database:

	$ python manage.py syncdb

