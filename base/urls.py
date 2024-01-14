from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("tasks/", views.tasks, name="tasks"),
    path("createtask/", views.createTask, name="create-task"),
    path("updatetask/<str:pk>/", views.updateTask, name="update-task"),
    path("deletetask/<str:pk>/", views.deleteTask, name="delete-task"),
]
