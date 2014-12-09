from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from monitor import models

from crontab import CronTab
import os

class Command(BaseCommand):

	help = 'Installs cron tasks for the monitor.'
	

	def handle(self, *args, **options):

		monitor_list = models.Monitor.objects.all()
		virtualenv = os.environ.get('VIRTUAL_ENV', None)
		virtualenv_command = 'export PATH=%s/bin:/usr/local/bin:/usr/bin:/bin' % (virtualenv)
		tab = CronTab()

		for monitor in monitor_list:
			django_command = "&& python %s/manage.py fetcher_droid %s >> /var/log/mondroid/%s.fetcher.log" % (settings.BASE_DIR, monitor.slug, monitor.slug)

			if virtualenv:
				command = '%s %s' % (virtualenv_command, django_command)
			else:
				command = '%s' % (django_command)

			cron_job = tab.new(command)
			cron_job.minute.every(5)


		tab.write()
		print tab.render()