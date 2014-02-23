from django.forms import widgets
from rest_framework import serializers
from evenup_app.models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
	events = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail')

	class Meta:
		model = User
		field = ('id', 'username', 'phone','events')


class BillSplitSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.Field(source='owner.name')
	item = serializers.Field(source='item.description')
	class Meta:
		model = BillSplit
		fields = ('id', 'owner', 'item', 'amount')

class EventBillItemSerializer(serializers.HyperlinkedModelSerializer):
	bill_item_splits = BillSplitSerializer(many=True, required=False)
	class Meta:
		model = EventBillItem
		fields = ('id', 'cost', 'description', 'bill_item_splits')



class EventMemberSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer(many=False)
	event_member_purchased_items = EventBillItemSerializer(many=True, required=False)
	
	class Meta:
		model = EventMember
		fields = ('id',  'user', 'event_member_purchased_items')

class EventBillSerializer(serializers.HyperlinkedModelSerializer):
	event_bill_items = EventBillItemSerializer(many=True, required=False)
	class Meta:
		model = EventBill
		fields = ('id', 'event_bill_items')

class EventSerializer(serializers.HyperlinkedModelSerializer):
	event_members = EventMemberSerializer(many=True, required=False)
	event_bill = EventBillSerializer(many=False, required=False)
	class Meta:
		model = Event
		fields = ('id', 'title', 'description', 'is_active', 'created', 'event_members', 'event_bill')



class EventChargeSerializer(serializers.HyperlinkedModelSerializer):
	member = serializers.Field(source='member.phone')
	bill = serializers.Field(source='bill.event.title')
	class Meta:
		model = EventCharge
		fields = ('id', 'member', 'bill', 'amount_due', 'is_active', 'paid_time')
