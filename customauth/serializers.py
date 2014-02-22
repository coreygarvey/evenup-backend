from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    events = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail')

    class Meta:
        model = User
        field = ('id', 'email', 'phone', 'events', 'password')