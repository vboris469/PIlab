from django.db import models
from django.contrib.auth.models import User


class Serial(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Episode(models.Model):
    serial = models.ForeignKey(Serial)
    name = models.CharField(max_length=50)
    order = models.IntegerField(null=True)
    season = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Link(models.Model):
    episode = models.ForeignKey(Episode)
    link = models.CharField(max_length=150)

    def __unicode__(self):
        return self.link


class SerialWatching(models.Model):
    serial = models.ForeignKey(Serial)
    user = models.ForeignKey(User, related_name='watching')
    order = models.IntegerField(default=0)


class Comment(models.Model):
    page = models.CharField(max_length=50)
    user_name = models.CharField(max_length=30)
    text = models.CharField(max_length=500)
