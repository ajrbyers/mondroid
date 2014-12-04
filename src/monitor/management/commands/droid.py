from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from monitor import models

import datetime
import requests

def send_email(downtime, up):
	emails = [u.email for u in User.objects.filter(is_staff=True)]
	if up:
		content = '%s is now back online.' % (downtime.monitor.name)
	else:
		content = '%s is experiencing an outage.' % (downtime.monitor.name)

	send_mail('Monitor Notification', content, settings.FROM_ADDRESS, emails)


class Command(BaseCommand):

	help = 'Runs Requests against monitors and creates Check object and, if the service is down, handles DownTimes.'
	

	def handle(self, *args, **options):
		monitor_list = models.Monitor.objects.all()

		for mon in monitor_list:
			try:
				r = requests.get(mon.url, verify=False)
				print r.status_code
				if r.status_code == 200:
					status = True
				else:
					status = False

				check = models.Check.objects.create(monitor=mon, status_code=r.status_code, history=r.history, elapsed_time=r.elapsed, up=status)
			except requests.ConnectionError:
				check = models.Check.objects.create(monitor=mon, status_code='521', history='Failed', elapsed_time='Failed', up=False)

			if mon.current_state:
				if not check.up and not mon.current_state.up:
					downtime, c = models.DownTime.objects.get_or_create(monitor=mon, active=True)
					downtime.checks.add(check)
				elif not check.up:
					downtime = models.DownTime.objects.create(monitor=mon, active=True)
					downtime.checks.add(check)
					downtime.save()
					send_email(downtime, False)
				elif check.up and not mon.current_state.up:
					downtime = models.DownTime.objects.get(monitor=mon, active=True)
					downtime.active = False
					downtime.save()
					send_email(downtime, True)

			mon.current_state = check
			mon.save() 