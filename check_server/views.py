from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from .tasks import manitor_server

# Create your views here.


def check_task(request: HttpRequest):
    task = manitor_server.delay()
    return JsonResponse({"task": task.id})