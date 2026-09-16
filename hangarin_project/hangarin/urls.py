from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_board, name="task_board"),
]