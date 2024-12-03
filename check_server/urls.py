from django.urls import path
from .views import (
    check_task,
    index,
    user_login,
    user_logout,
    camera,
    add_server,
    applications,
    add_apps,
    add_domain,
    app_info,
    add_docker,
    docker_info,
)

urlpatterns = [
    path("check", check_task),
    path("", index),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("device", camera, name="camera"),
    path("add-server", add_server, name="add-server"),
    path("apps/<int:server_id>/", applications, name="applications"),
    path("add-apps", add_apps, name="add-applications"),
    path("add-domain", add_domain, name="add-domain"),
    path("add-docker", add_docker, name="add-domain"),
    path("app-info/<int:app_id>", app_info, name="app-info"),
    path("docker-info/<int:app_id>", docker_info, name="docker-info"),
]
