from django.contrib import admin
from .models import Task, Weather, News

# Register your models here.

admin.site.register(Task)
admin.site.register(Weather)
admin.site.register(News)
