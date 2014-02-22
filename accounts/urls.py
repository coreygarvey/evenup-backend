from django.conf.urls import patterns, url, include
from accounts import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'accounts', views.AccountViewSet)


urlpatterns = patterns('',
	url(r'^', include(router.urls)),
)

