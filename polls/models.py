from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class Poll(models.Model):
    user = models.ForeignKey(User)
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    created_date = models.DateField('Created Date', default=datetime.date.today())
    last_updated_date = models.DateField('Last updated date', auto_now=True)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    voted_user = models.ManyToManyField(User, blank=True, null=True)

    def __unicode__(self):
        return self.choice_text
