from evenup_app.models import *
from evenup_app.serializers import *
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import link

from evenup_app.permissions import *
from rest_framework import viewsets
from django.contrib.auth import get_user_model

User = get_user_model()
@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'events': reverse('event-list', request=request, format=format)
		})

class EventViewSet(viewsets.ModelViewSet):
	model = Event
	serializer_class = EventSerializer
	permission_classes = (IsEventMember,)


	def get_queryset(self):
		"""
		This view should return a list of all the purchases
		for the currently authenticated user.
		"""
		user = self.request.user
		return Event.objects.filter(event_members__user=user)
	def pre_save(self, obj):
		
		obj.owner = self.request.user

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class EventMemberViewSet(viewsets.ModelViewSet):
	model = EventMember
	serializer_class = EventMemberSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly,)
	def get_queryset(self):
		"""
		This view should return a list of all the purchases
		for the currently authenticated user.
		"""
		user = self.request.user
		return EventMember.objects.filter(event=self.kwargs['event_pk'])

	def pre_save(self, obj):
		event = Event.objects.get(pk=self.kwargs['event_pk'])
		obj.event = event
		phone = obj.phone
		print phone
		user = User.objects.get(phone=phone)
		if user:
			obj.user = user



class EventBillItemViewSet(viewsets.ModelViewSet):
	queryset = EventBillItem.objects.all()
	serializer_class = EventBillItemSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsPurchaserOrReadOnly,)


	def pre_save(self, obj):
		event = Event.objects.get(pk=self.kwargs['event_pk'])
		user = self.request.user
		event_members = event.event_members.all()
		for member in event_members:
			if member.user.email == user.email:
				purchaser = member
		obj.purchaser = purchaser
		obj.bill = EventBill.objects.get(event=event)
	





class BillSplitViewSet(viewsets.ModelViewSet):
	queryset = BillSplit.objects.all()
	serializer_class = BillSplitSerializer
	permission_classes = (IsSplitOwner,)


	def pre_save(self, obj):
		print 'great'
		event_members=EventMember.objects.filter(event=self.kwargs['event_pk'])
		for member in event_members.all():
			if member.user == self.request.user:
				obj.owner = member
		item = EventBillItem.objects.get(pk=self.kwargs['billitem_pk'])
		obj.item = item
		obj.amount = (item.cost)/(item.bill_item_splits.all().count()+1)
		
		for split in item.bill_item_splits.all():
			split.amount = (item.cost)/(item.bill_item_splits.all().count()+1)
			split.save()

class EventChargeViewSet(viewsets.ModelViewSet):
	queryset = EventCharge.objects.all()
	serializer_class = EventChargeSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, MyUserPermissions,)

class EventBillViewSet(viewsets.ModelViewSet):
	queryset = EventBill.objects.all()
	serializer_class = EventBillSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, MyUserPermissions,)


