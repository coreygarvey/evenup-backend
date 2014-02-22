from evenup_app.models import Event
from evenup_app.serializers import EventSerializer
from evenup_app.serializers import UserSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import link
from django.contrib.auth.models import User
from evenup_app.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets


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
