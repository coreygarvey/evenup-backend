from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow owners of an object to edit it.
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		print 'hey'
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the owner

		return obj.owner == request.user

class IsUserOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow owners of an object to edit it.
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the owner

		return obj.user == request.user


class IsPurchaserOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow owners of an object to edit it.
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the owner

		return obj.purchaser == request.user

class IsEventMember(permissions.BasePermission):
	"""
	Custom permission to only allow owners of an object to edit it.
	"""
	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		user = request.user
		print 'hey'

		for event_member in obj.event_members.all():
			print event_member.user.email
			print user
			if event_member.user.email == user.email:
				print True
				return True

			else:
				return False

class IsSplitOwner(permissions.BasePermission):
	"""
	Custom permission to only allow owners of an object to edit it.
	"""
	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		user = request.user
		split_owner = obj.owner
		event_memberships = user.event_memberships.all()
		for event_member in event_memberships:
			if event_member == split_owner:

				return True
		return False


class MyUserPermissions(permissions.BasePermission):
    """
    Handles permissions for users.  The basic rules are

     - owner may GET, PUT, POST, DELETE
     - nobody else can access
     """

    def has_object_permission(self, request, view, obj):

        # check if user is owner
        return request.user == obj



