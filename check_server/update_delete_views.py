from .models import Server, Application, DockerApplication, Domain
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from email.parser import BytesParser
from email.policy import default
import json


def convert_form_data(request):
    raw_body = request.body

    content_type = request.headers.get("Content-Type")
    boundary = content_type.split("boundary=")[-1]
    full_boundary = f"--{boundary}".encode()

    parsed_data = {}
    parts = raw_body.split(full_boundary)

    for part in parts:

        part = part.strip()
        if not part or part == b"--":
            continue

        message = BytesParser(policy=default).parsebytes(part)
        content_disposition = message.get("Content-Disposition")

        if content_disposition:

            name = content_disposition.params.get("name")

            value = message.get_payload(decode=True).decode().strip()
            parsed_data[name] = value

    return parsed_data


@login_required
def get_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    print(server)
    return JsonResponse(
        {
            "name": server.name,
            "ssh_port": server.ssh_port,
            "ipv4": server.ipv4,
            "username": server.username,
        }
    )


@login_required
def get_app(request, app_id):
    if request.method == "GET":
        app = get_object_or_404(Application, id=app_id)
        data = {
            "name_run_on_server": app.name_run_on_server,
            "port": app.port,
        }
        return JsonResponse(data)


@login_required
def get_docker_info(request, app_id):
    if request.method == "GET":
        app = get_object_or_404(DockerApplication, id=app_id)
        data = {
            "name_run_on_docker": app.name_run_on_docker,
            "container_name": app.container_name,
            "port": app.port,
        }
        return JsonResponse(data)


@login_required
def get_domain_info(request, app_id):
    if request.method == "GET":
        app = get_object_or_404(Domain, id=app_id)
        data = {
            "domain": app.domain,
        }
        return JsonResponse(data)


@csrf_exempt
@login_required
def update_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)

    if request.method == "PUT":
        data = convert_form_data(request)
        print(data)
        server.name = data.get("name", server.name)
        server.ssh_port = data.get("ssh_port", server.ssh_port)
        server.ipv4 = data.get("ipv4", server.ipv4)
        server.username = data.get("username", server.username)
        server.password = data.get("password", server.password)
        server.save()
        return JsonResponse({"success": True, "message": "Server updated successfully"})
    elif request.method == "DELETE":
        server.delete()
        return JsonResponse({"success": True, "message": "Server deleted successfully"})


@csrf_exempt
@login_required
def update_app(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    if request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        app.name_run_on_server = data.get("name_run_on_server", app.name_run_on_server)
        app.port = data.get("port", app.port)

        app.save()
        return JsonResponse({"success": True, "message": "Server updated successfully"})
    elif request.method == "DELETE":
        app.delete()
        return JsonResponse({"success": True, "message": "Server deleted successfully"})


@csrf_exempt
@login_required
def update_docker_app(request, app_id):
    app = get_object_or_404(DockerApplication, id=app_id)
    print(request.method)
    if request.method == "PUT" or request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        app.name_run_on_docker = data.get("name_run_on_docker", app.name_run_on_docker)
        app.container_name = data.get("container_name", app.name_run_on_docker)
        app.port = data.get("port", app.port)

        app.save()
        return JsonResponse({"success": True, "message": "Server updated successfully"})
    elif request.method == "DELETE":
        app.delete()
        return JsonResponse({"success": True, "message": "Server deleted successfully"})


@csrf_exempt
@login_required
def update_domain(request, app_id):
    domain = get_object_or_404(Domain, id=app_id)
    print(request.method)
    if request.method == "PUT" or request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        domain.domain = data.get("domain", domain.domain)
        domain.save()

        return JsonResponse({"success": True, "message": "Server updated successfully"})
    elif request.method == "DELETE":
        domain.delete()
        return JsonResponse({"success": True, "message": "Server deleted successfully"})
