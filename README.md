# mondroid

Simple monitoring system written in Python/Django using requests.

## installation

Clone repo:

	$ git clone https://github.com/ajrbyers/mondroid.git

If you use [virtualenv](https://virtualenvwrapper.readthedocs.org/en/latest/), 
create a new virtualenv and switch to it. This is recommended.

Install requirements:

	$ sudo apt-get install sqlite3
	$ pip install -r requirements.txt

Make your own settings file:

	$ cp src/core/dev_settings.py src/core/settings.py

Create a database:

	$ python manage.py syncdb

An example cron job comes with the project in the file `cronjob.example`. 
The paths in this file should be changed to match your own, but it can then be 
installed with:

	$ crontab <name-of-your-cronjob-file>

To verify it was correctly installed, use:

	$ crontab -l

