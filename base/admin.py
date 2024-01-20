from django.contrib import admin
from .models import Task, Weather

# Register your models here.

admin.site.register(Task)
admin.site.register(Weather)
