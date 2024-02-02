from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Task database
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    event_date = models.DateTimeField(null=False, default=timezone.now)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            str(self.topic)
            + ": "
            + str(self.event_date)
            + "/ "
            + str(self.start_time)
            + " to "
            + str(self.end_time)
        )


# Weather database
class Weather(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, default="None")
    # temperature = models.TextField(max_length=100, default="None")
    # condition = models.TextField(max_length=100, default="None")
    # wind = models.TextField(max_length=100, default="None")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ": Weather in " + str(self.location)


# News database
class News(models.Model):
    # choices within the model to prevent unwanted choices added into the database by mistake
    NEW_SOURCE = [
        # data, displayed readable source in dropdown
        ("bbc_news", "BBC News"),
        ("cnn", "CNN News"),
        ("nbc_news", "NBC News"),
        ("abc_news", "ABC News"),
        ("the-washington-post", "The Washington Post"),
        ("espn", "ESPN"),
        ("associated-press", "Associated Press"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=50, choices=NEW_SOURCE)
    topic = models.TextField(max_length=100, default="general")

    def __str__(self):
        return str(self.user) + ": " + self.source + ", " + self.topic
