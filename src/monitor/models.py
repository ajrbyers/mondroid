from django.db import models
from datetime import datetime
from django.utils import timezone

class Monitor(models.Model):
	name = models.CharField(max_length=200, help_text="A Monitor's display name.")
	url = models.URLField(max_length=2000, unique=True, help_text="The URL to be monitored.")

	@property
	def current_state(self):
		return self.check_set.first()

	def time_in_state(self):
		"""returns a timedelta object between now and the most recent change in 
		the up/down state. 
		
		If this monitor has never had a change in this state, it returns how 
		long the state has been running.
		
		If there is no state history it returns None.
		
		"""
		# find the first state different to the current state
		if not self.current_state:
			# we have nothing to play with
			return None
		
		#now = datetime.now() # TZ naive
		now = timezone.now() # TZ aware
		# first state that is the opposite of current state
		next_state = self.check_set.filter(up = not self.current_state.up).first()
		if not next_state:
			# there has never been a difference in state
			next_state = self.check_set.last()
		return now - next_state.capture
		
	def __repr__(self):
		return '<Monitor %s>' % self.name

	def __unicode__(self):
		return u'%s' % (self.name,)

class Check(models.Model):
	monitor = models.ForeignKey(Monitor)
	status_code = models.CharField(max_length=10)
	history = models.CharField(max_length=2000)
	elapsed_time = models.CharField(max_length=200)
	up = models.BooleanField(default=True)
	capture = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-capture',)

	def up_or_down(self):
		return "up" if self.up else "down"

	def __repr__(self):
		return '<Check %s %s "%s">' % (self.monitor, self.capture.strftime("%Y-%m-%dT%H:%M:%S"), self.up_or_down())

	def __unicode__(self):
		return u' %s %s' % (self.monitor, self.status_code)

class DownTime(models.Model):
	monitor = models.ForeignKey(Monitor)
	checks = models.ManyToManyField(Check)
	active = models.BooleanField(default=True)
	starts = models.DateTimeField(auto_now=True, editable=True)
