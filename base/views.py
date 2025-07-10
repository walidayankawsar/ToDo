from django.views.generic.list import ListView
from .models import Task



# Create your views here.
class TaskList(ListView):
    model = Task
    context_object_name = "tasks"
