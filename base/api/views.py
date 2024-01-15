from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Task
from django.contrib.auth.models import User
from .serializers import TaskSerializer


# Show the available routes for the api
@api_view(["GET"])
def getRoutes(request):
    routes = [
        "GET /api",
        "GET /api/tasks/:id",
    ]
    return Response(routes)


# get the tasks from specific user
@api_view(["GET"])
def getTasks(request, pk):
    user = User.objects.get(id=pk)
    tasks = user.task_set.all()
    # Serialize object 'Task'
    serializer = TaskSerializer(tasks, many=True)
    # return serialize data
    return Response(serializer.data)
