import re
from typing import Any
from django import forms
from .models import Server, Application, Domain, DockerApplication
from .check_functions import is_server_alive, is_port_open, check_ssl_certificate
from .connect_server import ssh_connect


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ["name", "ssh_port", "ipv4", "username", "password", "company"]

    def clean_ipv4(self):
        ipv4 = self.cleaned_data.get("ipv4")

        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        if ipv4 and not re.match(ip_pattern, ipv4):
            raise forms.ValidationError("Invalid IP address format.")

        if not is_server_alive(ipv4):
            raise forms.ValidationError("Non-existent or non-working server IP address")

        return ipv4

    def clean(self) -> dict[str, Any]:

        data = super().clean()
        ipv4 = data.get("ipv4")
        username = data.get("username")
        password = data.get("password")
        port = data.get("ssh_port")
        if not ssh_connect(ip=ipv4, username=username, password=password, port=port):
            raise forms.ValidationError("Incorrect username or password")
        return data


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name_run_on_server", "company", "server", "port"]


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ["domain", "company", "server"]


class DockerApplication(forms.ModelForm):

    class Meta:
        model = DockerApplication
        fields = ["name_run_on_docker", "container_name", "company", "server", "port"]
