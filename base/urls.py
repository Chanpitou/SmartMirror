from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("tasks/", views.tasks, name="tasks"),
    path("createtask/", views.createTask, name="create-task"),
]
