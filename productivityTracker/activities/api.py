from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.authorization import Authorization
from tastypie import fields
from django.contrib.auth.models import User
from django.conf.urls import url
from models import Activity, ActivityLog, Target


class JsonResource(ModelResource):
    def determine_format(self, request):
        return 'application/json'


class UsersResource(JsonResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        excludes = ['is_staff', 'is_superuser', 'date_joined', 'last_login', 'password']


class ActivitiesResource(JsonResource):
    user = fields.ForeignKey(UsersResource, 'user', full=True)

    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activities'
        authorization = Authorization()


class LogsResource(JsonResource):
    user = fields.ForeignKey(UsersResource, 'user')

    class Meta:
        queryset = ActivityLog.objects.all()
        resource_name = 'logs'

    def prepend_urls(self):
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