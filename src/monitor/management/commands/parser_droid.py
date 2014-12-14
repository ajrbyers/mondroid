from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from monitor import models
from monitor import logic

import datetime
import requests
import json

def timedelta_milliseconds(td):
    return td.days*86400000 + td.seconds*1000 + td.microseconds/1000

def send_email(downtime, up):
	emails = [u.email for u in User.objects.filter(is_staff=True)]
	content = logic.render_email_content(up, downtime)

	send_mail('Monitor Notification', content, settings.FROM_ADDRESS, emails, html_message=content)


class Command(BaseCommand):

	help = 'Reads fetcher_droid logs and creates checks.'
	

	def handle(self, *args, **options):
		monitor_list = models.Monitor.objects.all()

		for monitor in monitor_list:
			fetcher_log = '/var/log/mondroid/%s.fetcher.log' % (monitor.slug)
			try:
				log_list = [line.rstrip().strip("'") for line in open(fetcher_log)]
			except IOError:
				print 'No log file found. Either the fetcher has not run on a new monitor, or the file is missing.'

			for log_line in log_list:
				log = json.loads(log_line)

				if log['status'] == 200: 
					up = True 
				else: 
					up = False

				check, c = models.Check.objects.get_or_create(
					monitor=monitor, 
					capture=datetime.datetime.strptime(log['date_time'], "%Y-%m-%d %H:%M:%S %Z"), 
					defaults={'status_code': log['status'], 
					'elapsed_time': float(log['elapsed']), 
					'history': log['history'], 
					'up': up})