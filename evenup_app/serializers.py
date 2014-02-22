from django.forms import widgets
from rest_framework import serializers
from evenup_app.models import Event
from django.contrib.auth.models import User

class EventSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source='owner.username')
    class Meta:
        model = Event
        fields = ('id', 'owner', 'title', 'description', 'is_active')

class UserSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        field = ('id', 'username', 'events')