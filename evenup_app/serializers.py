from django.forms import widgets
from rest_framework import serializers
from evenup_app.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class EventSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.phone')
    class Meta:
        model = Event
        fields = ('id', 'owner', 'title', 'description', 'is_active')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    events = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail')

    class Meta:
        model = User
        field = ('id', 'username', 'events')

class EventMemberSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.Field(source='user.phone')
    class Meta:
        model = EventMember
        fields = ('id', 'user', 'event',)


class EventBillItemSerializer(serializers.HyperlinkedModelSerializer):
    purchaser = serializers.Field(source='purchaser.first_name')
    class Meta:
        model = EventBillItem
        fields = ('id', 'cost', 'description')

class BillSplitSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.first_name')
    item = serializers.Field(source='item.description')
    class Meta:
        model = BillSplit
        fields = ('id', 'owner', 'item')
