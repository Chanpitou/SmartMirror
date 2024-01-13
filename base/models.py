from django.db import models


# Create your models here.
class Task(models.Model):
    topic = models.CharField(max_length=200)
    description = models.TextField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.topic) + ": " + str(self.description[0:500])
