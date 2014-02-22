from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from customauth.models import MyUser

# Create your models here.



User = get_user_model()


class Account(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True, related_name='account')
	stripe_customer_id = models.CharField(max_length=100)
	stripe_recipient_id = models.CharField(max_length=100)

	class Meta:
		ordering = ('created',)
	def create_user_account(sender, instance, created, **kwargs):
		if created:
			Account.objects.create(owner=instance)

	post_save.connect(create_user_account, sender=MyUser)
	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(Account, self).save(*args, **kwargs)

transaction_types = (
    ('deposit', 'deposit'),
    ('withdrawal', 'withdrawal'),
)
transaction_statuses = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('failed', 'failed'),
)
class AccountTransaction(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	transaction_type = models.CharField(max_length=1, choices=transaction_types)
	account = models.ForeignKey(Account, related_name='account-transaction')
	amount = models.IntegerField()
	transaction_status = models.CharField(max_length=1, choices=transaction_statuses)
	stripe_transaction_id = models.CharField(max_length=100)


	class Meta:
		ordering = ('created',)
	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""

		super(AccountTransaction, self).save(*args, **kwargs)