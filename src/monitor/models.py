from django.db import models

class Monitor(models.Model):
	name = models.CharField(max_length=200, help_text="A Monitor's display name.")
	url = models.URLField(max_length=2000, help_text="The URL to be monitored.")
	current_state = models.ForeignKey('Check', related_name='current_state', null=True, blank=True)

	def __repr__(self):
		return '%s' % (self.name)

	def __unicode__(self):
		return u'%s' % (self.name)

class Check(models.Model):
	monitor = models.ForeignKey(Monitor)
	status_code = models.CharField(max_length=10)
	history = models.CharField(max_length=2000)
	elapsed_time = models.CharField(max_length=200)
	up = models.BooleanField(default=True)
	capture = models.DateTimeField(auto_now=True)

	def __repr__(self):
		return '%s %s' % (self.monitor, self.status_code)

	def __unicode__(self):
		return u' %s %s' % (self.monitor, self.status_code)

class DownTime(models.Model):
	monitor = models.ForeignKey(Monitor)
	checks = models.ManyToManyField(Check)
	active = models.BooleanField(default=True)
	starts = models.DateTimeField(auto_now=True, editable=True)