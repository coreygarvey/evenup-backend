from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)
from django.conf import settings

from rest_framework.authtoken.models import Token
# Create your models here.



User = get_user_model()
for user in User.objects.all():
	Token.objects.get_or_create(user=user)

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)




class Event(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=50, blank=True, default='')
	description = models.CharField(max_length=100, blank=True, default='')
	is_active = models.BooleanField(default=False)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='events')

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(Event, self).save(*args, **kwargs)