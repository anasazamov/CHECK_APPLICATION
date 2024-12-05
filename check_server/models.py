from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Company(models.Model):

    name = models.CharField(max_length=50)
    chanel_id = models.CharField(max_length=50)
    user = models.ManyToManyField(to=User)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Server(models.Model):

    name = models.CharField(max_length=50)
    ssh_port = models.IntegerField(default=22)
    ipv4 = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=150)
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)

    class Meta:

        unique_together = ["ipv4", "username"]

    def __str__(self) -> str:
        return self.name


class Application(models.Model):

    name_run_on_server = models.CharField(max_length=50)
    port = models.IntegerField(default=0)
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE)
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)

    class Meta:
        ordering = ["port"]

    def __str__(self) -> str:
        return self.name_run_on_server

    class Meta:
        unique_together = ["port", "server"]


class DockerApplication(models.Model):
    name_run_on_docker = models.CharField(max_length=50)
    container_name = models.CharField(max_length=50)
    port = models.IntegerField(default=0)
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE)
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.container_name} {self.port}"

    class Meta:
        unique_together = ["port", "server", "container_name"]


class Domain(models.Model):
    domain = models.CharField(max_length=50)
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE)
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.domain

    class Meta:
        unique_together = ["server", "domain"]


class Alert(models.Model):

    time = models.DateTimeField()
    server = models.ForeignKey(to=Server, on_delete=models.SET_NULL, null=True)
    application = models.ForeignKey(
        to=Application, on_delete=models.SET_NULL, null=True
    )
    domain = models.ForeignKey(to=Domain, on_delete=models.SET_NULL, null=True)
    docker = models.ForeignKey(
        to=DockerApplication, on_delete=models.SET_NULL, null=True
    )
