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

from evenup_app.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountViewSet(viewsets.ModelViewSet):
	queryset = Account.objects.all()
	serializer_class = AccountSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


	def pre_save(self, obj):
		obj.owner = self.request.user

