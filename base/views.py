from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


# Create your views here.
def index(request):
    context = {}
    return render(request, "base/index.html", context)


# Rendering all task to the task page
def tasks(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "base/tasks.html", context)


# Creating new tasks
def createTask(request):
    form = TaskForm()
    if request.method == "POST":
        Task.objects.create(
            topic=request.POST.get("task-topic"),
            description=request.POST.get("task-description"),
        )
        return redirect("tasks")

    context = {}
    return render(request, "base/create_task.html", context)
