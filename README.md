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

Mondroid comes with a command that will install droid fetch commands into your Crontab. You should run this command as the user you want to fetch the results.

	$ python manage.py install_droids go

This command will create a cron command for each of your monitors. You can run it again to add new monitors once you've created them. These "droids" will run requests against your server and then record the checks in log files located in /var/log/mondroid/.

The command will also install a job for the parser droid, this droid consumes the log files and creates new checks.

You can test the crontab output by running:

	$ python manage.py install_droids test

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

This assumes Ubuntu 14.04, distribution's standard Nginx, 
[uWSGI](https://uwsgi-docs.readthedocs.org/en/latest/) and a clone of the repo 
in `/srv/mondroid/`.

Install the new dependencies:

	$ sudo apt-get install nginx-full python-dev && sudo pip install 'uwsgi>=2.0.8'

Provided is an [example nginx vhost](nginx-vhost.conf.example). Copy it across
and tweak the settings as necessary:

	$ sudo cp /srv/mondroid/nginx-vhost.conf.example /etc/nginx/sites-available/mondoid.conf
	$ sudo vim /etc/nginx/sites-available/mondoid.conf
	
Enable the site:

	$ sudo ln -s /etc/nginx/sites-available/mondoid.conf /etc/nginx/sites-enabled/mondoid.conf

_Before_ you restart Nginx you will need to configure uWSGI. uWSGI is highly 
configurable, but a good starting point is available in the [example uwsgi.ini]
(uwsgi.ini.example) file provided. Copy the file across and update as necessary.

	$ cp uwsgi.ini.example uwsgi.ini
	$ vim uwsgi.ini
	
_Ensure the `virtualenv` param is correctly set!_

Start uWSGI:

	$ cd /srv/mondroid
	$ sudo uwsgi -d --ini uwsgi.ini
	$ sudo service nginx restart

