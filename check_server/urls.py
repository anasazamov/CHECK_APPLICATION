from django.urls import path
from .views import check_task
urlpatterns = [
    path("", check_task)
]