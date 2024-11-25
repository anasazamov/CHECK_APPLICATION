from django.urls import path
from .views import check_task, index, user_login, user_logout, camera, add_server
urlpatterns = [
    path("check", check_task),
    path("", index),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path("device", camera, name='camera'),
    path("add-server", add_server, name='add-server'),

]