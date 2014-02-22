from django.conf.urls import patterns, url, include
from evenup_app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', views.EventViewSet)



urlpatterns = patterns('',
	url(r'^', include(router.urls)),
	url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

