from django.db import models

# Create your models here.

class Account(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	stripe_customer_id = models.CharField(max_length=100, blank=True, default='')
	stripe_recipient_id = models.CharField(max_length=100, blank=True, default='')

	class Meta:
		ordering = ('created',)

class Event(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=50, blank=True, default='')
	description = models.CharField(max_length=100, blank=True, default='')
	is_active = models.BooleanField(default=False)
	owner = models.ForeignKey('auth.User', related_name='events')

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(Event, self).save(*args, **kwargs)