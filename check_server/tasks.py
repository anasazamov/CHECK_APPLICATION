from core.celery import app
from .models import Server, Application

@app.task
async def manitor_server():
    servers = Server.objects.all().values("ip", "username", "password")