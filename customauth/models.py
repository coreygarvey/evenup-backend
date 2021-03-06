from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)



class MyUserManager(BaseUserManager):
	def create_user(self, email, phone, first_name, last_name, password):
		"""
		Creates and saves a User with the given email, phone and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			phone=phone,
			first_name=first_name,
			last_name=last_name,
			password=password
		)
		user.set_password(password)
		user.save(using=self._db)
		user_profile = UserProfile.objects.create(user=user)
		user_profile.save()
		return user

	def create_superuser(self, email, phone, first_name, last_name, password):
		"""
		Creates and saves a superuser with the given email, date of birth and password.
		"""
		user = self.create_user(email,
			password=password,
			phone=phone,
			first_name=first_name,
			last_name=last_name
			)
		user.is_admin = True
		user.save(using=self._db)
		user_profile = UserProfile.objects.create(user=user)
		user_profile.save()
		return user


class MyUser(AbstractBaseUser):
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	phone = models.CharField(
		max_length=255,
		unique=True)
	first_name = models.CharField(
		max_length=30
		)
	last_name = models.CharField(
		max_length=30
		)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

	def get_full_name(self):
		# The user is identified by their email address
		return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.email

	def __str__(self):              # __unicode__ on Python 2
		return self.email

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

class UserProfile(models.Model):  
	created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(MyUser, related_name='user-profile')
	#profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

	def __unicode__(self):
		return u'Profile of user: %s' % self.user.username
