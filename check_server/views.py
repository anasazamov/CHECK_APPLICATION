from .forms import ServerForm
from django.shortcuts import render
from django.http.request import HttpRequest
from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from .models import Server, Application, Company
from .tasks import manitor_server, check_domain_ssl
from django.contrib.auth.decorators import login_required
from .check_functions import is_server_alive, is_port_open, check_ssl_certificate

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/') 
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):

        
    name = request.GET.get("name", "")
    user = request.user
    company = Company.objects.filter(user=user)

    servers = Server.objects.filter(company__in=company, name__contains=name).values("id", "name", "ipv4")
    for server in servers:
        is_active = is_server_alive(server['ipv4'])
        server["is_active"] = is_active
    
    return render(request, "index.html", {"servers": servers, "name": name})

@login_required
def add_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()  # serverni saqlash
            return JsonResponse({"success": True, "message": "Server successfully added!"})
        else:
            return JsonResponse({"success": False, "message": form.errors})
    else:
        form = ServerForm()

    return render(request, 'add_server.html', {'form': form})


def camera(request):
    return render(request, 'applications.html', {})
  

def check_task(request: HttpRequest):
    task = check_domain_ssl.delay()
    manitor_server.delay()
    return JsonResponse({"task": task.id})