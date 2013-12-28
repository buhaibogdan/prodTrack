from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=120, blank=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class ActivityLog(models.Model):
    activity = models.ForeignKey(Activity)
    user = models.ForeignKey(User)
    minutes_logged = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s logged on %s %s minutes" % (self.user, self.activity, self.minutes_logged)


class Target(models.Model):
    activity = models.ForeignKey(Activity)
    user = models.ForeignKey(User)
    target_hours = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __unicode__(self):
        return "Targe %s hours until %s" % (self.target_hours, self.end_date)