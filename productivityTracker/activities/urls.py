from django.conf.urls import patterns, url, include
from tastypie.api import Api
from . import api

v1_api = Api(api_name='v1')
v1_api.register(api.ActivitiesResource())
v1_api.register(api.LogsResource())
v1_api.register(api.UsersResource())
v1_api.register(api.TargetsResource())

urlpatterns = patterns('',
                       url(r'^', include(v1_api.urls)))