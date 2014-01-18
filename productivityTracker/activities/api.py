from django.contrib.auth import authenticate, login, logout
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.authorization import Authorization
from tastypie.http import HttpForbidden, HttpUnauthorized
from tastypie import fields
from django.contrib.auth.models import User
from django.conf.urls import url
from models import Activity, ActivityLog, Target


class JsonResource(ModelResource):
    datesRegEx = r"^(?P<resource_name>%s)/(?P<start_date>[\d]{4}-[\d]{1,2}-[\d]{1,2})," \
                 r"(?P<end_date>[\d]{4}-[\d]{1,2}-[\d]{1,2})%s$"

    def determine_format(self, request):
        return 'application/json'

    def serialize_queryset(self, query_set, request):
        bundles = [self.build_bundle(item, request=request) for item in query_set]
        return [self.full_dehydrate(bundle) for bundle in bundles]


class UsersResource(JsonResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        excludes = ['is_staff', 'is_superuser', 'date_joined', 'last_login', 'password']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        print request.POST
        username = request.POST.get('username', 'bb')
        password = request.POST.get('password', 'bb')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {'success': True})
            return self.create_response(request, {
                'success': False,
                'reason': 'disabled',
            }, HttpForbidden)
        return self.create_response(request, {
            'success': False,
            'reason': 'incorrect'
        }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if request.user and request.user.is_authenticated:
            logout(request)
            return self.create_response(request, {'success': True})
        return self.create_response(request, {'success': False}, HttpUnauthorized)


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
    activity = fields.ForeignKey(ActivitiesResource, 'activity')

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

        start_date = kwargs['start_date']
        end_date = kwargs['end_date']

        query_set = ActivityLog.objects.filter(created_at__gte=start_date, created_at__lte=end_date)
        data = self.serialize_queryset(query_set, request)

        return self.create_response(request, data)