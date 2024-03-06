from django.shortcuts import render, redirect
from .models import Event, Weather, News, MirrorDisplay, SecretKey
from .forms import (
    EventForm,
    UserForm,
    RegisterForm,
    DisplayForm,
    LocationForm,
    NewsForm,
)

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

import secrets, string, time
import requests


# Create User login
def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    form = UserForm()
    # get inputed username and password
    if request.method == "POST":
        form = UserForm(request.POST)
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        # check if the inputed user exist, otherwise throw out a flash error
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Username or password does not match.")
        except:
            messages.error(request, "User does not exist.")

        # use username and password to authenticate, then login the user

    context = {"page": page, "form": form}
    return render(request, "base/login_register.html", context)


# Create logout user
def logoutUser(request):
    logout(request)
    return redirect("home")


# generating unique secret key for each user
def generate_random_code(min_length=12, max_length=16):
    # Define the pool of characters to choose from
    characters = string.ascii_letters + string.digits

    # Generate a random length between min_length and max_length
    length = secrets.choice(range(min_length, max_length + 1))

    # Generate the random code
    random_code = "".join(secrets.choice(characters) for _ in range(length))

    return random_code


# Register user
def registerPage(request):
    form = RegisterForm()
    secretKey = generate_random_code()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            mirror_display, created = MirrorDisplay.objects.get_or_create(user=user)
            mirror_display.save()
            user_location, created = Weather.objects.get_or_create(user=user)
            user_location.save()
            user_news, created = News.objects.get_or_create(user=user)
            user_news.save()
            user_key, created = SecretKey.objects.get_or_create(
                user=user, secret_key=secretKey
            )
            user_key.save()
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
@login_required(login_url="login")
def aboutPage(request):
    return render(request, "base/about.html")


# Go to location page to update the current location
def updateLocation(request):
    user = request.user
    user_weather = Weather.objects.get(user=user)
    user_location = user_weather.location
    form = LocationForm(
        initial={
            "lf_location": user_weather.location,
        }
    )
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            user_weather.location = form.cleaned_data["lf_location"]
            user_weather.save()

            return redirect("configuration")
    context = {"form": form}
    return render(request, "base/location.html", context)


# navbar -- setup page
@login_required(login_url="login")
def setupPage(request):
    user = request.user
    secretkey = SecretKey.objects.get(user=user)
    context = {"user": user, "secretkey": secretkey}
    return render(request, "base/setup.html", context)


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
    # form = NewsForm()
    user = request.user
    user_news = News.objects.get(user=user)
    form = NewsForm(
        initial={
            "nf_source": user_news.source,
            "nf_topic": user_news.topic,
        }
    )
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            user_news.source = form.cleaned_data["nf_source"]
            user_news.topic = form.cleaned_data["nf_topic"]
            user_news.save()

            return redirect("configuration")
    context = {"form": form}
    return render(request, "base/news.html", context)


# Mirror Display choices
def mirrorDisplay(request, pk):
    displays = [
        "Default",
        "Display 2",
        "Display 3",
        "Display 4",
        "Display 5",
        "Display 6",
    ]
    user = request.user
    user_display = MirrorDisplay.objects.get(user=user)
    form = DisplayForm(
        initial={
            "md_display": user_display.display,
        }
    )
    if request.method == "POST":
        form = DisplayForm(request.POST)
        if form.is_valid():
            user_display.display = form.cleaned_data["md_display"]
            user_display.save()
            return redirect("configuration")
    context = {"form": form, "displays": displays}
    return render(request, "base/mirror_display.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Mirror configuration
def configurationPage(request):
    # Weather Section
    response = ""
    wind = ""
    CITY = ""
    user = request.user
    user_display = MirrorDisplay.objects.get(user=user)
    mirror_display = user_display.display

    WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?"
    Weather_API_KEY = "5321674b7863f1cae6a2dcda7ab0322d"

    CITY = Weather.objects.filter(user=user).values_list("location", flat=True).first()

    try:
        url = WEATHER_URL + "appid=" + Weather_API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        weather = response["weather"][0]
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
        "weather": weather,
        "news_source": news_source,
        "news_topic": news_topic,
        "mirror_display": mirror_display,
    }
    return render(request, "base/configuration.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Rendering all task to the task page
def event(request, pk):
    user = User.objects.get(id=pk)
    events = user.event_set.all()
    dark = "dark"
    context = {"events": events, "dark": dark}
    return render(request, "base/events.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Creating new events
def createEvent(request):
    page = "create"
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        # When using form instead ModelForm, always check validation first
        if form.is_valid():
            ev_topic = form.cleaned_data["ev_topic"]
            ev_description = form.cleaned_data["ev_description"]
            ev_location = form.cleaned_data["ev_location"]
            ev_date = form.cleaned_data["ev_date"]
            ev_start_time = form.cleaned_data["ev_start_time"]
            ev_end_time = form.cleaned_data["ev_end_time"]
            try:
                ev = Event.objects.create(
                    user=request.user,
                    topic=ev_topic,
                    description=ev_description,
                    location=ev_location,
                    event_date=ev_date,
                    start_time=ev_start_time,
                    end_time=ev_end_time,
                )
                return redirect("events", pk=request.user.pk)

            except Exception as e:
                messages.error(request, f"Error creating event: {e}")

    context = {"form": form, "page": page}
    return render(request, "base/create_event.html", context)


# restrict user if not authenticated
@login_required(login_url="login")
# Creating new events
def updateEvent(request, pk):
    page = "update"

    event = Event.objects.get(id=pk)
    # Populate the form with initial data from the existing event
    form = EventForm(
        initial={
            "ev_topic": event.topic,
            "ev_description": event.description,
            "ev_location": event.location,
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
            event.location = form.cleaned_data["ev_location"]
            event.event_date = form.cleaned_data["ev_date"]
            event.start_time = form.cleaned_data["ev_start_time"]
            event.end_time = form.cleaned_data["ev_end_time"]
            event.save()
            return redirect("events", pk=request.user.id)

    context = {"form": form, "page": page}
    return render(request, "base/create_event.html", context)


login_required(login_url="login")


# duplicate event
def duplicateEvent(request, pk):
    page = "duplicate"

    user = request.user
    event = Event.objects.get(id=pk)

    form = EventForm(
        initial={
            "ev_topic": event.topic,
            "ev_description": event.description,
            "ev_location": event.location,
            "ev_date": event.event_date,
            "ev_start_time": event.start_time,
            "ev_end_time": event.end_time,
        }
    )
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            ev_topic = form.cleaned_data["ev_topic"]
            ev_description = form.cleaned_data["ev_description"]
            ev_location = form.cleaned_data["ev_location"]
            ev_date = form.cleaned_data["ev_date"]
            ev_start_time = form.cleaned_data["ev_start_time"]
            ev_end_time = form.cleaned_data["ev_end_time"]
            try:
                ev = Event.objects.create(
                    user=request.user,
                    topic=ev_topic,
                    description=ev_description,
                    location=ev_location,
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
# deleting event
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
