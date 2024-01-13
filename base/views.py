from django.shortcuts import render
from .models import Task


# Create your views here.
def index(request):
    context = {}
    return render(request, "base/index.html", context)


def tasks(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "base/tasks.html", context)
