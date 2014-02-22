from evenup_app.models import Event
from evenup_app.serializers import EventSerializer
from evenup_app.serializers import UserSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User


class EventList(generics.ListCreateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def pre_save(self, obj):
		obj.owner = self.request.user

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Event.objects.all()
	serial_class = EventSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def pre_save(self, obj):
		obj.owner = self.request.user

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer