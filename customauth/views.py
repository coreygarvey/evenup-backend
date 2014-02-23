from evenup_app.models import Event
from evenup_app.models import EventMember
from evenup_app.serializers import EventSerializer
from evenup_app.serializers import UserSerializer
from rest_framework import mixins
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import link
from django.views.decorators.csrf import csrf_exempt

from evenup_app.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from django.contrib.auth import get_user_model

User = get_user_model()

from django.views.decorators.csrf import ensure_csrf_cookie


class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer


# Create your views here.
@api_view(['POST'])
def create_user(request):

	  serialized = UserSerializer(context={'request': request},data=request.DATA)
	  if serialized.is_valid():
		  created_user = User.objects.create_user(
			  serialized.init_data['email'],
			  serialized.init_data['phone'],
			  serialized.init_data['first_name'],
			  serialized.init_data['last_name'],
			  serialized.init_data['password'],
		  )
		  print created_user
		  eventmembers=EventMember.objects.all()
		  for member in eventmembers:
		  	print member.phone
		  	print 'middle'
		  	print created_user.phone
		  	if member.phone == created_user.phone:
		  		print created_user
		  		print member
		  		member.user=created_user
		  		member.save()
		  return Response(serialized.data, status=status.HTTP_201_CREATED)
	  else:
		  return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

