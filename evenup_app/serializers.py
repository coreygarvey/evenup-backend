from django.forms import widgets
from rest_framework import serializers
from evenup_app.models import Event
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
        model = Event
        fields = ('id', 'user', 'event',)