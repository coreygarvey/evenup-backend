from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)
from django.conf import settings
from accounts.models import Account
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
	is_active = models.BooleanField(default=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='events')

	class Meta:
		ordering = ('created',)

	
	def create_charges_and_payables(self):
		for member in self.event_members.all():
			paid = 0
			for item in member.event_member_purchased_items.all():
				paid += item.cost
			to_pay = 0
			for split in member.user_bill_splits.all():
				to_pay += split.amount
			net = paid - to_pay
			print net
			if net >= 0:
				EventPayable.objects.create(bill=self.event_bill, member=member, amount_paid=0,amount_owed=net)
			if net < 0:
				EventCharge.objects.create(bill=self.event_bill, member=member, amount_due=net, is_active=True)


	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(Event, self).save(*args, **kwargs)

class EventMember(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='event_memberships', null=True)
	event = models.ForeignKey(Event, related_name='event_members')
	name = models.CharField(max_length=50, blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)

	class Meta:
		ordering = ('created',)


	def create_event_member(sender, instance, created, **kwargs):
		user = instance.owner
		phone = instance.owner.phone
		name = user.first_name + ' ' + user.last_name
		if created:
			EventMember.objects.create(event=instance, user=user, name=name, phone=phone)



	post_save.connect(create_event_member, sender=Event)


	def total_owed(self):
		total = 0
		for item in self.event_member_purchased_items:
			total += item.cost
		return total

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
	bill = models.ForeignKey(EventBill, related_name='event_bill_items')
	purchaser = models.ForeignKey(EventMember, related_name='event_member_purchased_items')
	cost = models.IntegerField()
	description = models.CharField(max_length=100)
	user_splitter = models.BooleanField(default=False)
	

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
	owner = models.ForeignKey(EventMember, related_name='user_bill_splits')
	amount = models.IntegerField(null=True, blank=True)
	

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(BillSplit, self).save(*args, **kwargs)

	def create_purchaser_split(sender, instance, created, **kwargs):
		print instance
		print instance.purchaser
		print instance.cost
		if created:
			BillSplit.objects.create(item=instance, owner=instance.purchaser, amount=instance.cost)
	post_save.connect(create_purchaser_split, sender=EventBillItem)



class EventCharge(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	bill = models.ForeignKey(EventBill, related_name='event_charges')
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

class EventPayable(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	bill = models.ForeignKey(EventBill, related_name='event_payables')
	member = models.ForeignKey(EventMember, related_name='event_payables')
	amount_paid = models.IntegerField(null=True, blank=True)
	amount_owed = models.IntegerField(null=True, blank=True)
	

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(EventPayable, self).save(*args, **kwargs)

ea_transaction_types = (
    ('charge', 'charge'),
    ('payable', 'payable'),
)

class EventAccountTransaction(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	charge = models.ForeignKey(EventCharge, related_name='event_account_transaction_charges', unique=True, null=True)
	payable = models.ForeignKey(EventPayable, related_name='event_account_transaction_payables', unique=True, null=True)
	account = models.ForeignKey(Account, related_name='event_account_transaction')
	ea_transaction_type = models.CharField(max_length=1, choices=ea_transaction_types)
	amount = models.IntegerField()
	

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(EventAccountTransaction, self).save(*args, **kwargs)



ea_transaction_types = (
    ('charge', 'charge'),
    ('payable', 'payable'),
)


class AccountTransaction(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	account_transaction_type = models.DateTimeField(auto_now_add=True)
	charge = models.ForeignKey(EventCharge, related_name='account_transaction_charges', unique=True, null=True)
	payable = models.ForeignKey(EventPayable, related_name='account_transaction_payables', unique=True, null=True)
	account = models.ForeignKey(Account, related_name='account_transaction')
	ea_transaction_type = models.CharField(max_length=1, choices=ea_transaction_types)
	amount = models.IntegerField()
	

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(AccountTransaction, self).save(*args, **kwargs)