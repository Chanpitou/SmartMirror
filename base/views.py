from django.shortcuts import render, redirect
from .models import Event, Weather, News
from .forms import EventForm, UserForm

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


# navbar -- about page
def aboutPage(request):
    return render(request, "base/about.html")


# Go to location page to update the current location
def updateLocation(request):
    user = request.user
    if request.method == "POST":
        input_location = request.POST.get("user_location")
        loc, created = Weather.objects.get_or_create(user=user)
        if loc is not None:
            loc.location = input_location
            loc.save()
            return redirect("configuration")

    return render(request, "base/location.html")


# Go to News page to change the source or topic
def updateNews(request):
    news_sources = [
        "BBC",
        "CNN News",
        "NBC News",
        "ABC News",
        "The Washington Post",
        "ESPN",
        "Associated Press",
    ]
    user = request.user

    if request.method == "POST":
        news_source = request.POST.get("news_source")
        news_topic = request.POST.get("news_topic")

        # retrieve or create an News instance for user
        news_instance, created = News.objects.get_or_create(user=request.user)

        if news_instance is not None:
            news_instance.source = news_source
            news_instance.topic = news_topic
            news_instance.save()
            return redirect("configuration")
    context = {"news_sources": news_sources}
    return render(request, "base/news.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Mirror configuration
def configurationPage(request):
    # Weather Section
    # Fetching/displaying Weather API
    response = ""
    wind = ""
    CITY = ""
    user = request.user

    WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?"
    Weather_API_KEY = "5321674b7863f1cae6a2dcda7ab0322d"

    CITY = Weather.objects.filter(user=user).values_list("location", flat=True).first()

    try:
        url = WEATHER_URL + "appid=" + Weather_API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        wind = response["wind"]
    except:
        messages.error(request, "City not found, please check/update again.")

    # News section
    news_source = (
        News.objects.filter(user=request.user).values_list("source", flat=True).first()
    )
    news_topic = (
        News.objects.filter(user=request.user).values_list("topic", flat=True).first()
    )

    context = {
        "response": response,
        "wind": wind,
        "news_source": news_source,
        "news_topic": news_topic,
    }
    return render(request, "base/configuration.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Rendering all task to the task page
def event(request, pk):
    user = User.objects.get(id=pk)
    events = user.event_set.all()
    context = {"events": events}
    return render(request, "base/events.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Creating new events
def createEvent(request):
    page = "create"
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            ev_topic = form.cleaned_data["ev_topic"]
            ev_description = form.cleaned_data["ev_description"]
            ev_date = form.cleaned_data["ev_date"]
            ev_start_time = form.cleaned_data["ev_start_time"]
            ev_end_time = form.cleaned_data["ev_end_time"]
            try:
                ev = Event.objects.create(
                    user=request.user,
                    topic=ev_topic,
                    description=ev_description,
                    event_date=ev_date,
                    start_time=ev_start_time,
                    end_time=ev_end_time,
                )
                return redirect("events", pk=request.user.pk)

            except Exception as e:
                print(f"Error creating event: {e}")

    context = {"form": form, "page": page}
    return render(request, "base/create_event.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Creating new events
def updateEvent(request, pk):
    event = Event.objects.get(id=pk)
    # Populate the form with initial data from the existing event
    form = EventForm(
        initial={
            "ev_topic": event.topic,
            "ev_description": event.description,
            "ev_date": event.event_date,
            "ev_start_time": event.start_time,
            "ev_end_time": event.end_time,
        }
    )
    # When submited
    if request.method == "POST":
        # Create an instance of form with the data submitted via POST request
        form = EventForm(request.POST)
        if form.is_valid():
            # Update the existing event with the form data
            event.topic = form.cleaned_data["ev_topic"]
            event.description = form.cleaned_data["ev_description"]
            event.event_date = form.cleaned_data["ev_date"]
            event.start_time = form.cleaned_data["ev_start_time"]
            event.end_time = form.cleaned_data["ev_end_time"]
            event.save()
            return redirect("events", pk=request.user.id)

    context = {"form": form}
    return render(request, "base/create_event.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Creating new events
def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == "POST":
        event.delete()
        messages.success(
            request, f"Event '{event.topic}' has been successfully deleted."
        )
        return redirect("events", pk=request.user.id)
    context = {"obj": event.topic}
    return render(request, "base/delete_event.html", context)
