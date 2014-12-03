from django.contrib.auth import authenticate, logout, login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from monitor import models

def index(request):

	context = {}
	template = 'monitor/index.html'

	return render(request, template, context)

@login_required
def dashboard(request):

	monitor_list = models.Monitor.objects.all().order_by('name')
	downtime_list = models.DownTime.objects.all().filter(active=True)

	context = {
		'monitor_list': monitor_list,
		'downtime_list': downtime_list,
	}
	template = 'monitor/dashboard.html'

	return render(request, template, context)

def user_login(request):

	if request.user.is_authenticated():
		messages.info(request, 'You are already logged in.')
		return redirect(reverse('monitor_dashboard'))

	if request.POST:
		user = request.POST.get('user_name')
		pawd = request.POST.get('user_pass')

		user = authenticate(username=user, password=pawd)

		if user is not None:
			if user.is_active:
				login(request, user)
				messages.info(request, 'Login successful.')
				if request.GET.get('next'):
					return redirect(request.GET.get('next'))
				else:
					return redirect(reverse('monitor_dashboard'))
			else:
				messages.add_message(request, messages.INFO, 'User account is not active.')
		else:
			messages.add_message(request, messages.INFO, 'Account not found with those details.')

	context = {}
	template = 'login.html'

	return render(request, template, context)

def user_logout(request):

	messages.info(request, 'You have been logged out.')
	logout(request)

	return redirect(reverse('monitor_index'))