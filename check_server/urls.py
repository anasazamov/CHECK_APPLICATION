from django.urls import path
from .update_delete_views import (
    get_server,
    update_server,
    get_app,
    update_app,
    get_docker_info,
    update_docker_app,
    get_domain_info,
    update_domain,
)
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
    path("servers/<int:server_id>/", get_server, name="get-server"),
    path("servers/<int:server_id>/update/", update_server, name="update-server"),
    path("apps/<int:server_id>/", applications, name="applications"),
    path("app/<int:app_id>/", get_app, name="get-applications-info"),
    path("apps/<int:app_id>/update/", update_app, name="update-application"),
    path("add-apps", add_apps, name="add-applications"),
    path("add-domain", add_domain, name="add-domain"),
    path("add-docker", add_docker, name="add-domain"),
    path("app-info/<int:app_id>", app_info, name="app-info"),
    path("docker-info/<int:app_id>", docker_info, name="docker-info"),
    path("docker-apps/<int:app_id>/", get_docker_info, name="get-docker-info"),
    path(
        "docker-apps/<int:app_id>/update/", update_docker_app, name="update-docker-app"
    ),
    path("domains/<int:app_id>/", get_domain_info, name="get-domain"),
    path("domains/<int:app_id>/update/", update_domain, name="update-domain"),
]
