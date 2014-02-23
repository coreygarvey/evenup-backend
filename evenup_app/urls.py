from django.conf.urls import patterns, url, include
from evenup_app import views
from rest_framework.routers import DefaultRouter

from rest_framework_nested import routers
from django.contrib import admin
admin.autodiscover()

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'events', views.EventMemberViewSet)

nested_router = routers.SimpleRouter()
nested_router.register(r'events', views.EventViewSet)
billitems_router = routers.NestedSimpleRouter(nested_router, r'events', lookup='event')
billitems_router.register(r'billitems', views.EventBillItemViewSet)




urlpatterns = patterns('',
	url(r'^', include(router.urls)),
	url(r'^', include(billitems_router.urls)),
	url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^admin/', include(admin.site.urls)),
)

