from accounts.models import Account
from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Account
        field = ('id', 'owner' )