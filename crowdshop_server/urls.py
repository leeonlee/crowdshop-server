from django.conf.urls import patterns, include, url
from rest_framework import routers
from crowdshop import views
from crowdshop.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crowdshop_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include('crowdshop.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
