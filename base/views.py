from django.shortcuts import render
from . import models


# Create your views here.
def index(request):
    chores = models.Todo.objects.all()
    context = {"chores": chores}
    return render(request, "base/main.html", context)

