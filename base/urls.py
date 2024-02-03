from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("", views.index, name="home"),
    path("events/<str:pk>/", views.event, name="events"),
    path("createEvent/", views.createEvent, name="create-event"),
    path("updateEvent/<str:pk>/", views.updateEvent, name="update-event"),
    path("deleteEvent/<str:pk>/", views.deleteEvent, name="delete-event"),
    path("about/", views.aboutPage, name="about"),
    path("configuration/", views.configurationPage, name="configuration"),
    path("location/", views.updateLocation, name="location"),
    path("news/", views.updateNews, name="news"),
]
