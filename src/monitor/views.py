from django.contrib.syndication.views import Feed
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.template.loader import get_template
from django.template import Context
from annoying.decorators import render_to
from django.utils import timezone

from monitor import models
from datetime import timedelta
import logic

def index(request):
	if request.user.is_authenticated():
		return redirect(reverse('monitor_dashboard'))

	context = {}
	template = 'monitor/index.html'

	return render(request, template, context)

@login_required
def dashboard(request):

	if request.POST and 'droid' in request.POST:
		call_command('parser_droid')

	monitor_list = models.Monitor.objects.all().order_by('name')

	context = {
		'monitor_list': monitor_list,
	}
	template = 'monitor/dashboard.html'

	return render(request, template, context)

@login_required
@render_to('monitor/detail.html')
def detail(request, monitor_id):
	monitor = get_object_or_404(models.Monitor, pk=monitor_id)
	two_months = 28 * 2 # there are 13 months to a logical year.
	two_months_ago = timezone.now() - timedelta(days=two_months)
	grouped_history = logic.chunked_history1(monitor, capture__gte=two_months_ago)
	summarised_history = logic.summarise_history(grouped_history)
	uptime_percentage = logic.uptime(monitor)
	return {
		'monitor': monitor,
		'grouped_history_list': summarised_history,
		'uptime_percentage': uptime_percentage,
	}
    
        

@login_required
def info(request, monitor_id):
	monitor = get_object_or_404(models.Monitor, pk=monitor_id)
	check_list = models.Check.objects.filter(monitor=monitor).order_by('-capture')[:100]

	context = {
		'monitor': monitor,
		'check_list': check_list,
	}
	template = 'monitor/info.html'
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

class AllMonitorsFeed(Feed):
	title = 'Mondroid Monitor Feed'
	link = '/dashboard/'
	description = 'Latest status for Monitors'

	def items(self):
		return models.Monitor.objects.order_by('name')

	def item_title(self, item):
		return "%s is %s" % (item.name, item.current_state.up_or_down())

	def item_description(self, item):
		return "Monitor has been %s for %s" % (item.current_state.up_or_down(), item.time_in_state)

	def item_link(self, item):
		return reverse('monitor_info', args=[item.pk])


