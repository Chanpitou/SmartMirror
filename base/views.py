from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm, UserForm

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Create User login
def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    # get inputed username and password
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        # check if the inputed user exist, otherwise throw out a flash error
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")

        # use username and password to authenticate, then login the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not match.")
    context = {"page": page}
    return render(request, "base/login_register.html", context)


# Create logout user
def logoutUser(request):
    logout(request)
    return redirect("home")


# Register user
def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured during registeration.")

    context = {"form": form}
    return render(request, "base/login_register.html", context)


# Create your views here.
def index(request):
    context = {}
    return render(request, "base/index.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Rendering all task to the task page
def tasks(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "base/tasks.html", context)


# navbar -- about page
def aboutPage(request):
    return render(request, "base/about.html")


# restrict user if not authenticated
@login_required(login_url="login")
# Mirror configuration
def configurationPage(request):
    return render(request, "base/configuration.html")


# restrict user if not authenticated
@login_required(login_url="login")
# Creating new tasks
def createTask(request):
    # form = TaskForm()
    if request.method == "POST":
        Task.objects.create(
            topic=request.POST.get("task-topic"),
            description=request.POST.get("task-description"),
        )
        return redirect("tasks")

    context = {}
    return render(request, "base/create_task.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Update task
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == "POST":
        task.topic = request.POST.get("topic")
        task.description = request.POST.get("description")
        task.save()
        return redirect("tasks")
    context = {"form": form}
    return render(request, "base/update_task.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Delete task
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")
    context = {"obj": task}
    return render(request, "base/delete_task.html", context)
