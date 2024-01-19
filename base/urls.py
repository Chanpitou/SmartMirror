from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("", views.index, name="home"),
    path("tasks/<str:pk>/", views.tasks, name="tasks"),
    path("createtask/", views.createTask, name="create-task"),
    path("updatetask/<str:pk>/", views.updateTask, name="update-task"),
    path("deletetask/<str:pk>/", views.deleteTask, name="delete-task"),
    path("about/", views.aboutPage, name="about"),
    path("configuration/", views.configurationPage, name="configuration"),
    path("location/", views.updateLocation, name="location"),
]
