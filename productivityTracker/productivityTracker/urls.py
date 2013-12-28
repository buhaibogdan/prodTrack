from django.conf.urls import patterns, include, url

from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                       # maybe reconsider the next url regex
                       url(r'^', include('activities.urls', namespace='activity')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', view=views.index)
)
