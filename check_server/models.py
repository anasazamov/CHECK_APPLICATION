from django.db import models

# Create your models here.


class Server(models.Model):

    name = models.CharField(max_length=50)
    ssh_port = models.IntegerField(default=22)
    ip = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=150)

    class Meta:

        unique_together = ["ip", "username"]

class Application(models.Model):

    name_run_on_server = models.CharField(max_length=50)
    port = models.IntegerField(default=0)
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["port", "server"]

