from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from monitor import models
from monitor import logic

import datetime
import requests

def timedelta_milliseconds(td):
    return td.days*86400000 + td.seconds*1000 + td.microseconds/1000

def send_email(downtime, up):
	emails = [u.email for u in User.objects.filter(is_staff=True)]
	content = logic.render_email_content(up, downtime)

	send_mail('Monitor Notification', content, settings.FROM_ADDRESS, emails, html_message=content)


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

				time = timedelta_milliseconds(r.elapsed)

				check = models.Check.objects.create(monitor=mon, status_code=r.status_code, history=r.history, elapsed_time=time, up=status)
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
					downtime, c = models.DownTime.objects.get_or_create(monitor=mon, active=True)
					downtime.active = False
					downtime.save()
					send_email(downtime, True)

			mon.current_state = check
			mon.save() 