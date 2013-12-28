from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from models import Activity, ActivityLog, Target


class JsonResource(ModelResource):
    def determine_format(self, request):
        return 'application/json'


class ActivitiesResource(JsonResource):
    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activities'

    def determine_format(self, request):
        return 'application/json'


class LogsResource(JsonResource):
    class Meta:
        queryset = ActivityLog.objects.all()
        resource_name = 'logs'

    def determine_format(self, request):
        return 'application/json'


class UsersResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'