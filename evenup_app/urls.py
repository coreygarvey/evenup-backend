from django.conf.urls import patterns, url, include
from evenup_app import views
from rest_framework.routers import DefaultRouter

from rest_framework_nested import routers
from django.contrib import admin
admin.autodiscover()

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'events', views.EventMemberViewSet)

events_router = routers.SimpleRouter()
events_router.register(r'events', views.EventViewSet)

eventmembers_router = routers.NestedSimpleRouter(events_router, r'events', lookup='event')
eventmembers_router.register(r'eventmembers', views.EventMemberViewSet)

eventcharge_router = routers.NestedSimpleRouter(eventmembers_router, r'eventmembers', lookup='eventmember')
eventcharge_router.register(r'eventcharges', views.EventChargeViewSet)

billitems_router = routers.NestedSimpleRouter(events_router, r'events', lookup='event')
billitems_router.register(r'billitems', views.EventBillItemViewSet)

billsplit_router = routers.NestedSimpleRouter(billitems_router, r'billitems', lookup='billitem')
billsplit_router.register(r'billsplits', views.BillSplitViewSet)



urlpatterns = patterns('',
	url(r'^', include(router.urls)),
	url(r'^', include(eventmembers_router.urls)),
	url(r'^', include(eventcharge_router.urls)),
	url(r'^', include(billitems_router.urls)),
	url(r'^', include(billsplit_router.urls)),
	url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
	url(r'^admin/', include(admin.site.urls)),
)

