from django.contrib import admin
from .models import Event, Weather, News

# Register your models here.

admin.site.register(Event)
admin.site.register(Weather)
admin.site.register(News)
