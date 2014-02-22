from django.conf.urls import patterns, url, include
from customauth import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = patterns('',
	url(r'^', include(router.urls)),
	url(r'^signup/$', 'customauth.views.create_user'),
)

