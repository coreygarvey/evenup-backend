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

class EventMember(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='event_membership')
	event = models.ForeignKey(Event, related_name='event_member')

	class Meta:
		ordering = ('created',)

	def create_event_member(sender, instance, created, **kwargs):
		if created:
			EventMember.objects.create(event=instance, user=instance.owner)

	post_save.connect(create_event_member, sender=Event)

	

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(EventMember, self).save(*args, **kwargs)

class EventBill(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	event = models.OneToOneField(Event, related_name='event_bill')
	amount_paid = models.IntegerField(null=True, blank=True)
	amount_due = models.IntegerField(null=True, blank=True)
	

	class Meta:
		ordering = ('created',)

	def create_event_bill(sender, instance, created, **kwargs):
		if created:
			EventBill.objects.create(event=instance)

	post_save.connect(create_event_bill, sender=Event)

	

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(EventBill, self).save(*args, **kwargs)



class EventBillItem(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	bill = models.ForeignKey(EventBill, related_name='event_bill_items', unique=True)
	purchaser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='event_member_purchased_items')
	cost = models.IntegerField()
	description = models.CharField(max_length=100)
	

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(EventBillItem, self).save(*args, **kwargs)


class BillSplit(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	item = models.ForeignKey(EventBillItem, related_name='bill_item_splits')
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_bill_splits')
	amount = models.IntegerField()
	

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(BillSplit, self).save(*args, **kwargs)

	def create_purchaser_split(sender, instance, created, **kwargs):
		if created:
			BillSplit.objects.create(item=instance, owner=instance.purchaser, amount=instance.cost)
	post_save.connect(create_purchaser_split, sender=EventBillItem)

class EventCharge(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	bill = models.ForeignKey(EventBill, related_name='event_charges', unique=True)
	member = models.ForeignKey(EventMember, related_name='event_charges')
	amount_due = models.IntegerField()
	is_active = models.BooleanField(default=False)
	paid_time = models.DateTimeField(null=True, blank=True)
	

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(EventCharge, self).save(*args, **kwargs)

