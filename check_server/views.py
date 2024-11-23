from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from .tasks import manitor_server, check_domain_ssl

# Create your views here.


def check_task(request: HttpRequest):
    task = check_domain_ssl.delay()
    manitor_server.delay()
    return JsonResponse({"task": task.id})