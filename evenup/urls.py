from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'evenup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('evenup_app.urls')),
    url(r'^', include('customauth.urls')),
    url(r'^', include('accounts.urls')),
)
