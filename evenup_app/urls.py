from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from evenup_app import views
from django.conf.urls import include

urlpatterns = patterns('',
    url(r'^events/$', views.EventList.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += patterns('',
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)