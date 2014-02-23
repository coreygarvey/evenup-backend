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

from evenup_app.permissions import IsOwnerOrReadOnly
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
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


	def pre_save(self, obj):
		obj.owner = self.request.user

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class EventMemberViewSet(viewsets.ModelViewSet):
	queryset = EventMember.objects.all()
	serializer_class = EventMemberSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


	def pre_save(self, obj):
		obj.user = self.request.user

class EventBillItemViewSet(viewsets.ModelViewSet):
	queryset = EventBillItem.objects.all()
	serializer_class = EventBillItemSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


	def pre_save(self, obj):
		obj.purchaser = self.request.user
		event = Event.objects.get(pk=self.kwargs['event_pk'])
		obj.bill = EventBill.objects.get(event=event)


class BillSplitViewSet(viewsets.ModelViewSet):
	queryset = BillSplit.objects.all()
	serializer_class = BillSplitSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


	def pre_save(self, obj):
		obj.owner = self.request.user
		item = EventBillItem.objects.get(pk=self.kwargs['billitem_pk'])
		obj.item = item
		obj.amount = (item.cost)/(item.bill_item_splits.all().count())
		
		for split in item.bill_item_splits.all():
			split.amount = (item.cost)/(item.bill_item_splits.all().count())
			split.save()

