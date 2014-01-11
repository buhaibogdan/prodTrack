from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.authorization import Authorization
from tastypie import fields
from django.contrib.auth.models import User
from django.conf.urls import url
from models import Activity, ActivityLog, Target


class JsonResource(ModelResource):
    datesRegEx = r"^(?P<resource_name>%s)/(?P<start_date>[\d]{4}-[\d]{1,2}-[\d]{1,2})," \
                 r"(?P<end_date>[\d]{4}-[\d]{1,2}-[\d]{1,2})%s$"

    def determine_format(self, request):
        return 'application/json'


class UsersResource(JsonResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        excludes = ['is_staff', 'is_superuser', 'date_joined', 'last_login', 'password']

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        print 'haha'
        return self.create_response(request, { 'success': True })

    def logout(self, request, **kwargs):
        print "hihi"
        return self.create_response(request, { 'success': True })


class ActivitiesResource(JsonResource):
    user = fields.ForeignKey(UsersResource, 'user')

    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activities'
        authorization = Authorization()


class TargetsResource(JsonResource):
    user = fields.ForeignKey(UsersResource, 'user')
    activity = fields.ForeignKey(ActivitiesResource, 'activity')

    class Meta:
        queryset = Target.objects.all()
        resource_name = 'targets'
        authorization = Authorization()


class LogsResource(JsonResource):
    user = fields.ForeignKey(UsersResource, 'user')

    class Meta:
        queryset = ActivityLog.objects.all()
        resource_name = 'logs'

    def prepend_urls(self):
        return [
            url(JsonResource.datesRegEx %
                (self._meta.resource_name, trailing_slash()), self.wrap_view('get_logs_between_dates'),
                name='api_get_logs_between_dates'
                )
        ]

    def get_logs_between_dates(self, request, **kwargs):

        print kwargs['start_date']
        print kwargs['end_date']
        raise NotImplementedError()

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