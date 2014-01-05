from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from django.contrib.auth.models import User
from django.conf.urls import url
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

    def prepend_urls(self):
        # url(r"^(?P<resource_name>%s)/(?P<year>[\d]{4})/(?P<month>{1,2})/(?<day>[\d]{1,2})%s$"
        # % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list_with_date'),
        # name="api_dispatch_list_with_date"),
        # (?P<year>[\d]{4})-(?P<month>[\d]{1,2})-
        #                   (?P<day>[\d]{1,2})
        return [
            url(r"^(?P<resource_name>%s)/(?P<start_date>[\d]{4}-[\d]{1,2}-[\d]{1,2}),"
                r"(?P<end_date>[\d]{4}-[\d]{1,2}-[\d]{1,2})%s$" %
                (self._meta.resource_name, trailing_slash()), self.wrap_view('get_logs_between_dates'),
                name='api_get_logs_between_dates'
                )
        ]

    def get_logs_between_dates(self, request, **kwargs):
        print kwargs['start_date']
        print kwargs['end_date']

    def get_object_list(self, request):
        """
            Here we get the request params and retrieve the objects based on them.
        """
        try:
            startDate = request.GET['startDate']
            endDate = request.GET['endDate']
        except KeyError:
            pass
        return super(LogsResource, self).get_object_list(request)


class UsersResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'