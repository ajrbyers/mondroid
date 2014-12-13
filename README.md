# mondroid

Simple monitoring system written in Python/Django.

## installation

Clone repo:

	$ git clone https://github.com/ajrbyers/mondroid.git

### installing virtualenv

If you use [virtualenv](https://virtualenvwrapper.readthedocs.org/en/latest/), 
create a new virtualenv and switch to it. This is recommended.

	$ sudo pip install virtualenvwrapper

Append this to your `~/.bashrc` file
	
	export WORKON_HOME=$HOME/.virtualenvs
	source /usr/local/bin/virtualenvwrapper.sh
	export PIP_DOWNLOAD_CACHE=$HOME/.pip/download_cache
	
Create your virtualenv:
	
	$ mkvirtualenv mondroid

### installing mondroid

Install requirements:

	$ sudo apt-get install sqlite3
	$ pip install -r requirements.txt

Make your own settings file:

	$ cd src/
	$ cp core/dev_settings.py core/settings.py

Create a database:

	$ python manage.py syncdb

### installing a cronjob

An example cron job comes with the project in the file `cronjob.example`. 
The paths in this file should be changed to match your own, but it can then be 
installed with:

	$ crontab <name-of-your-cronjob-file>

To verify it was correctly installed, use:

	$ crontab -l

## running remotely on development server (__not__ recommended)

_Django's development server wasn't meant for production. No serious 
considerations for security or performance were made._

To have the development server accept requests from the world, use:

	$ python manage.py 0.0.0.0:8000
	
## running remotely on an Apache webserver

This assumes Ubuntu 14.04, Apache 2.2 and a clone of the repo in 
`/srv/mondroid/`.

	$ sudo apt-get install apache2 libapache2-mod-wsgi

Included is an [example Apache2 vhost](apache2.2-vhost.conf.example) that should
be installed and enabled with:

	$ sudo cp apache2.2-vhost.conf.example /etc/apache2/sites-available/mondroid.conf
	$ sudo a2ensite mondroid

The settings must then be fitted to your particular environment:

	$ sudo vim /etc/apache2/sites-available/mondroid.conf

Afterwards restart the Apache server:

	$ sudo service apache2 restart

Django requires static files to be collected into a single place to be served.

	$ cd /srv/mondroid/src/
	$ workon mondroid
	$ python manage.py collectstatic

## running remotely on an Nginx webserver


