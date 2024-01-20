from rest_framework.serializers import ModelSerializer
from base.models import Task, Weather
from rest_framework import serializers
from django.contrib.auth.models import User


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ("location", "created", "updated")


class UserSerializer(serializers.ModelSerializer):
    weather = WeatherSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "weather")


# class UserSerializer(serializers.ModelSerializer):
#     locations = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ("username", "email", "locations")

#     def get_locations(self, obj):
#         return Weather.objects.filter(user=obj).values_list("location", flat=True)
