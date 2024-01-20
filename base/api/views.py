from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Task, Weather
from django.contrib.auth.models import User
from .serializers import TaskSerializer, WeatherSerializer, UserSerializer


# Show the available routes for the api
@api_view(["GET"])
def getRoutes(request):
    routes = [
        "GET /api",
        "GET /api/tasks/:userid",
        "GET /api/location/:userid",
    ]
    return Response(routes)


# get the tasks from specific user
@api_view(["GET"])
def getTasks(request, pk):
    try:
        user = User.objects.get(id=pk)
        tasks = user.task_set.all()
        # Serialize object 'Task'
        serializer = TaskSerializer(tasks, many=True)
        # return serialize data
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# @api_view(["GET"])
# def getLocation(request, pk):
#     user_cur = User.objects.get(id=pk)
#     user_location = Weather.objects.filter(user=user_cur).values("user", "location")

#     serializer = WeatherSerializer(user_location, many=False)
#     return Response(serializer.data)


# views.py
@api_view(["GET"])
def getLocation(request, pk):
    try:
        user = User.objects.get(id=int(pk))
        serializer = UserSerializer(user)
        return Response(serializer.data)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
