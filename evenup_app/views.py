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
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
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

		print obj
		if obj.is_active == False:
			print 'hey'
			obj.create_charges_and_payables()

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
		event = self.kwargs['event_pk']
		user = self.request.user
		event_memberships = EventMember.objects.filter(event=self.kwargs['event_pk'])
		event_member = event_memberships.get(user=user)
		items = EventBillItem.objects.filter(bill__event=self.kwargs['event_pk'])
		print 'item'
		for item in items:
			print 'item'
			print item
			splits = item.bill_item_splits.all()
			for split in splits:
				if split.owner == event_member:
					item.user_splitter = True


		user = self.request.user
		return EventMember.objects.filter(event=self.kwargs['event_pk'])

	def pre_save(self, obj):
		event = Event.objects.get(pk=self.kwargs['event_pk'])
		obj.event = event
		phone = obj.phone
		print phone
		user = User.objects.filter(phone=phone)
		if len(user) != 0:
			obj.user = user[0]


class EventBillItemViewSet(viewsets.ModelViewSet):
	model = EventBillItem
	serializer_class = EventBillItemSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsPurchaserOrReadOnly,)


	def pre_save(self, obj):
		event = Event.objects.get(pk=self.kwargs['event_pk'])
		user = self.request.user
		event_members = event.event_members.all()
		for member in event_members:
			print member.name
			if member.phone == user.phone:
				purchaser = member
		obj.purchaser = purchaser
		obj.bill = EventBill.objects.get(event=event)
	def get_queryset(self):
		"""
		This view should return a list of all the purchases
		for the currently authenticated user.
		"""
		event = self.kwargs['event_pk']
		user = self.request.user
		event_memberships = EventMember.objects.filter(event=self.kwargs['event_pk'])
		event_member = event_memberships.get(user=user)
		items = EventBillItem.objects.filter(bill__event=self.kwargs['event_pk'])
		print 'item'
		for item in items:
			print 'item'
			print item
			splits = item.bill_item_splits.all()
			for split in splits:
				if split.owner == event_member:
					item.user_splitter = True
					
		return items






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

'''
distribute(amount)
	for event_payables in self.payables:
				payable
'''

class DeleteBillSplit(APIView):
	model = BillSplit
	"""
	List all snippets, or create a new snippet.
	"""
	def delete(self, request, *args, **kwargs):
		user = request.user
		event = Event.objects.get(pk=self.kwargs['event_pk'])
		event_memberships = EventMember.objects.filter(event=event)
		user_membership = event_memberships.get(user=user)
		item = EventBillItem.objects.get(pk=self.kwargs['pk'])
		splits = item.bill_item_splits.all()
		for split in splits:
			if split.owner == user_membership:
				split.delete()
		return Response('deleted')

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class ChargesAndPayables(APIView):
	model = Event
	"""
	List all snippets, or create a new snippet.
	"""
	def get(self, request,  *args, **kwargs):
		user = request.user

		event = Event.objects.get(pk=self.kwargs['event_pk'])
		event_members=EventMember.objects.filter(event=event)
		event_member=event_members.get(user=user)
		bill = event.event_bill
		event_charges = bill.event_charges.all()
		member_charge = event_charges.filter(member=event_member)
		if len(member_charges) != 0:
			serializer = EventChargeSerializer(member_charge[0])
			return JSONResponse(serializer.data)
		event_payables=bill.event_payables.all()
		member_payable = event_payables.filter(member=event_member)
		serializer = EventPayableSerializer(member_payable[0])
		return JSONResponse(serializer.data)
		


