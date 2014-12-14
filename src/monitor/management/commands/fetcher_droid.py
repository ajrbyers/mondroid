from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from monitor import models

import sys
import requests
import pprint
import json

monitor_slug = sys.argv[1:][1]

class Command(BaseCommand):

	help = 'Runs Requests against monitors and logs them.'
	

	def handle(self, *args, **options):

		monitor = models.Monitor.objects.get(slug=monitor_slug)
		request = requests.get(monitor.url)
		output = {
			'date_time': timezone.now().strftime("%Y-%m-%d %H:%M:%S %Z"),
			'status': request.status_code,
			'history': request.history,
			'elapsed': request.elapsed.total_seconds(),
		}

		pprint.pprint(json.dumps(output))

		