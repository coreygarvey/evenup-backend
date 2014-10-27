from django.conf.urls import patterns, url, include
from evenup_app import views
from rest_framework.routers import DefaultRouter

from rest_framework_nested import routers
from django.contrib import admin
admin.autodiscover()

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'events', views.EventMemberViewSet)

simple_router = routers.SimpleRouter()
simple_router.register(r'events', views.EventViewSet)


eventbills_router = routers.NestedSimpleRouter(simple_router, r'events', lookup='event')
eventbills_router.register(r'eventbills', views.EventBillViewSet)

eventmembers_router = routers.NestedSimpleRouter(simple_router, r'events', lookup='event')
eventmembers_router.register(r'eventmembers', views.EventMemberViewSet)

eventcharges_router = routers.NestedSimpleRouter(eventmembers_router, r'eventmembers', lookup='eventmember')
eventcharges_router.register(r'eventcharges', views.EventChargeViewSet)

billitems_router = routers.NestedSimpleRouter(simple_router, r'events', lookup='event')
billitems_router.register(r'billitems', views.EventBillItemViewSet)

billsplit_router = routers.NestedSimpleRouter(billitems_router, r'billitems', lookup='billitem')
billsplit_router.register(r'billsplits', views.BillSplitViewSet)

urlpatterns = patterns('',
	url(r'^', include(router.urls)),
	url(r'^', include(eventbills_router.urls)),
	url(r'^', include(eventmembers_router.urls)),
	url(r'^', include(eventcharges_router.urls)),
	url(r'^', include(billitems_router.urls)),
	url(r'^', include(billsplit_router.urls)),
	url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^events/(?P<event_pk>[0-9]+)/billitems/(?P<pk>[0-9]+)/billsplit_delete/$', views.DeleteBillSplit.as_view()),
	url(r'^events/(?P<event_pk>[0-9]+)/closed/$', views.ChargesAndPayables.as_view())
)

