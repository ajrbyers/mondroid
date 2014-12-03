from django.core.management.base import BaseCommand, CommandError
from monitor import models

import datetime
import requests


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

			if not check.up and not mon.current_state.up:
				print 'If we have a downtime, and the previous state was a downtime, record this in the DownTime.checks'
				downtime, c = models.DownTime.objects.get_or_create(monitor=mon, active=True)
				downtime.checks.add(check)
			elif not check.up:
				print 'Else if we have a downtime but the previous state was up, create a downtime.'
				downtime = models.Downtime(monitor=mon, active=True)
				downtime.checks.add(check)
				downtime.save()
			elif check.up and not mon.current_state.up:
				print 'Else if we we have an up state and the previous state was down, close down the previous downtime.'
				downtime = models.DownTime.objects.get(monitor=mon, active=True)
				downtime.active = False
				downtime.save()

			mon.current_state = check
			mon.save() 