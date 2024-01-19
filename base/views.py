from django.shortcuts import render, redirect
from .models import Task, Weather
from .forms import TaskForm, UserForm

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

import requests


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
def tasks(request, pk):
    user = User.objects.get(id=pk)
    tasks = user.task_set.all()
    context = {"tasks": tasks}
    return render(request, "base/tasks.html", context)


# navbar -- about page
def aboutPage(request):
    return render(request, "base/about.html")


# Updating user location
def location(request, pk):
    weather = Weather.objects.get(id=pk)
    user = request.user
    if request.method == "POST":
        userLocation, created = Weather.objects.get_or_created(user=user)
        weather.location = request.POST.get("user_location")

        return redirect("configuration", pk=request.user.id)
    context = {}
    return render(request, "base/update_city.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Mirror configuration
def configurationPage(request):
    # Fetching/displaying Weather API
    response = ""
    wind = ""
    user = request.user

    WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "5321674b7863f1cae6a2dcda7ab0322d"
    if request.method == "POST":
        CITY = request.POST.get("city_name")
        try:
            url = WEATHER_URL + "appid=" + API_KEY + "&q=" + CITY
            response = requests.get(url).json()
            wind = response["wind"]
        except:
            messages.error(request, "City not found, please check/update again.")

    context = {
        "response": response,
        "wind": wind,
    }
    return render(request, "base/configuration.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Creating new tasks
def createTask(request):
    if request.method == "POST":
        Task.objects.create(
            user=request.user,
            topic=request.POST.get("task-topic"),
            description=request.POST.get("task-description"),
        )
        return redirect("tasks", pk=request.user.id)

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
        return redirect("tasks", pk=request.user.id)
    context = {"form": form}
    return render(request, "base/update_task.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Delete task
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == "POST":
        task.delete()
        return redirect("user", pk=request.user.id)
    context = {"obj": task}
    return render(request, "base/delete_task.html", context)
