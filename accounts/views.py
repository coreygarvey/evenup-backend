from accounts.models import Account
from accounts.serializers import AccountSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import link
from rest_framework.views import APIView
from evenup_app.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from django.contrib.auth import get_user_model
import stripe
User = get_user_model()

class AccountViewSet(viewsets.ModelViewSet):
	model = Account
	serializer_class = AccountSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


	def pre_save(self, obj):
		obj.owner = self.request.user

	def get_queryset(self):
		"""
		This view should return a list of all the purchases
		for the currently authenticated user.
		"""
		user = self.request.user
		event_memberships = user.event_memberships.all()
		amount_due=0
		print event_memberships
		for membership in event_memberships:
			charges = membership.event_charges.all()
			
			for charge in charges:
				if charge.is_active == True:
					
					amount_due += membership.event_charges.amount_due
		account=user.account.all()
		print account
		account.amount_due=amount_due
		account.save()
		return user.account

class StripeCharge(APIView):
	model = Account
	"""
	List all snippets, or create a new snippet.
	"""
	def post(self, request,  *args, **kwargs):
		# Set your secret key: remember to change this to your live secret key in production
		# See your keys here https://manage.stripe.com/account
		stripe.api_key = "sk_test_3aMNJsprXJcMdh1KffsskjMB"

		# Get the credit card details submitted by the form
		token = request.POST['stripeToken']
		amount = request.Post['amount']
		amount = amount*100
		# Create the charge on Stripe's servers - this will charge the user's card
		try:
		  charge = stripe.Charge.create(
		      amount=amount, # amount in cents, again
		      currency="usd",
		      card=token,
		      description="Charge paid!"
		  )
		except stripe.CardError, e:
		  return Response('Looks like there was an error')
		  pass
		return Response('Congratulations')


'''		
create_account_transaction(amount, type):
if type == DEPOSIT:
self.create_stripe_charge(amount)
if type == WITHDRAWAL
self.create_stripe_transfer(amount)
create_stripe_charge(amount):
if self.stripe_customer_id is None:
self.create_stripe_customer():
call stripe(self.stripe_customer_id, amount) 
AccountTransaction.objects.create(type=deposit, account=self, amount=amount, status=pending)
if response.result == is_paid:
success_account_transaction(stripe_transaction)
else:
failure_account_transaction(stripe_transaction)
create_stripe_transfer(amount)
if self.stripe_recipient_id is None:
self.create_stripe_recipient()
call stripe(self.stripe_recipient_id, amount)
AccountTransaction.objects.create(type=withdrawal, account=self, amount=amount, status=pending)
if response.result == is_paid:
success_account_transaction(stripe_transaction)
else:
failure_account_transaction(stripe_transaction)
create_stripe_customer:  Credit Card Info or Token as Input
call stripe(token)
if created == True
self.stripe_customer_id=response.stripe_customer_id
else
return False
create_stripe_recipient Bank Account Info or Token as Input
call stripe(token)
if created == True
self.stripe_recipient_ide=response.stripe_recipient_id
else
return False
'''