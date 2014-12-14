from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from monitor import models

from crontab import CronTab
import os
import sys

try:
	action = sys.argv[1:][1]
except:
	action = ''

def find_job(tab, comment):
	for job in tab:
   		if job.comment == comment:
   			return job
   	return None

class Command(BaseCommand):

	help = 'Installs cron tasks for the monitor.'
	

	def handle(self, *args, **options):

		monitor_list = models.Monitor.objects.all()
		virtualenv = os.environ.get('VIRTUAL_ENV', None)
		tab = CronTab()

		for monitor in monitor_list:
			current_job = find_job(tab, "fetcher_droid_%s" % monitor.slug)

			if current_job == None:
				django_command = "&& python %s/manage.py fetcher_droid %s >> /var/log/mondroid/%s.fetcher.log" % (settings.BASE_DIR, monitor.slug, monitor.slug)

				if virtualenv:
					command = 'export PATH=%s/bin:/usr/local/bin:/usr/bin:/bin %s' % (virtualenv, django_command)
				else:
					command = '%s' % (django_command)

				cron_job = tab.new(command, comment="fetcher_droid_%s" % monitor.slug)
				cron_job.minute.every(5)

		# Install the parser droid command if it doesn't exist already
		current_job = find_job(tab, "parser_droid")
		if current_job == None:
			if virtualenv:
				command = 'export PATH=%s/bin:/usr/local/bin:/usr/bin:/bin && python %s/manage.py parser_droid' % (virtualenv, settings.BASE_DIR)
			cron_job = tab.new(command, comment="parser_droid")
			cron_job.minute.every(5)

		if action == 'test':
			print tab.render()
		elif action == 'quiet':
			pass
		else:
			tab.write()