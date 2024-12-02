from .forms import ServerForm, ApplicationForm, DomainForm
from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from .models import Server, Application, Company, Domain
from .tasks import manitor_server, check_domain_ssl, check_docker_app
from django.contrib.auth.decorators import login_required
from .check_functions import (
    is_server_alive,
    is_port_open,
    check_ssl_certificate,
    get_docker_ports_via_ssh,
    is_inner_port,
)
from .connect_server import ssh_connect, get_performance
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

# Create your views here.


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return render(
                    request,
                    "login.html",
                    {"form": form, "error": "Invalid username or password"},
                )
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def index(request):

    host_name = request.get_host()
    settings.DOMAIN = host_name
    name = request.GET.get("name", "")
    user = request.user
    company = Company.objects.filter(user=user)

    servers = Server.objects.filter(company__in=company, name__contains=name).values(
        "id", "name", "ipv4"
    )
    for server in servers:
        is_active = is_server_alive(server["ipv4"])
        server["is_active"] = is_active

    return render(request, "index.html", {"servers": servers, "name": name})


@login_required
def add_server(request):
    if request.method == "POST":
        data = request.POST.copy()
        data["company"] = Company.objects.filter(user=request.user).first().pk

        form = ServerForm(data)
        del data
        if form.is_valid():
            form.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": f"{form.data['name']} is successfully added!",
                }
            )
        else:
            return JsonResponse({"success": False, "message": form.errors})
    else:
        form = ServerForm()

    return render(request, "index.html", {"form": form})


@login_required
def applications(request, server_id):
    server = get_object_or_404(Server, id=server_id)

    name = request.GET.get("name", "")

    ssh = ssh_connect(server.ipv4, server.username, server.password, server.ssh_port)

    if ssh:
        performance = get_performance(ssh)
        docker_data = get_docker_ports_via_ssh(ssh)

    apps = (
        Application.objects.filter(server=server, name_run_on_server__contains=name)
        .select_related("server")
        .values("id", "name_run_on_server", "port", "server__ipv4")
    )
    for app in apps:
        is_active = is_port_open(app["server__ipv4"], app["port"])
        if not is_active:
            if ssh:
                is_active = is_inner_port(ssh, app["port"])

        app["is_active"] = is_active

    domains = Domain.objects.filter(server=server, domain__contains=name).values(
        "domain"
    )

    for domain in domains:
        check = check_ssl_certificate(domain["domain"])
        is_active = check["is_valid"]
        valid_to = check["valid_to"]
        days = (check["valid_to"] - datetime.now()).days
        domain["is_valid"] = is_active
        domain["valid_to"] = valid_to
        domain["days"] = days

    return render(
        request,
        "app.html",
        {
            "server": server,
            "apps": apps,
            "domains": domains,
            
        },
    )


@login_required
def add_apps(request):
    if request.method == "POST":

        data = request.POST
        form = ApplicationForm(data)

        if form.is_valid():
            form.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": f"{form.data['name_run_on_server']} is successfully added!",
                }
            )
        else:
            return JsonResponse({"success": False, "message": form.errors})
    else:
        form = Application()

    return render(request, "app.html", {"form": form})


@login_required
def add_domain(request):
    if request.method == "POST":

        data = request.POST
        form = DomainForm(data)

        if form.is_valid():
            form.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": f"{form.data['domain']} is successfully added!",
                }
            )
        else:
            return JsonResponse({"success": False, "message": form.errors})
    else:
        form = Application()

    return render(request, "apps.html", {"form": form})


@login_required
def camera(request):
    return render(request, "devices.html", {})


def check_task(request: HttpRequest):
    task = check_docker_app.delay()
    # manitor_server.delay()
    return JsonResponse({"task": task.id})
