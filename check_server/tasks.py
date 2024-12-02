from core.celery import app
from datetime import datetime
from .get_log import get_logs, get_logs_and_performance_by_port
from django.utils.timezone import now
from .connect_server import ssh_connect
from django.conf import settings
from .models import Server, Application, Alert, Domain, Company, DockerApplication
from .send_telegram_notifacation import send_alert_with_file, send_ssl_status
from .check_functions import (
    is_server_alive,
    is_port_open,
    check_ssl_certificate,
    get_docker_ports_via_ssh,
    is_inner_port
)

host_name = settings.ALLOWED_HOSTS


@app.task
def manitor_server():
    servers = (
        Server.objects.all()
        .select_related("company")
        .values(
            "id",
            "name",
            "ipv4",
            "username",
            "password",
            "ssh_port",
            "company__chanel_id",
        )
    )

    for server in servers:
        id = server["id"]
        ipv4 = server["ipv4"]
        username = server["username"]
        password = server["password"]
        ssh_port = server["ssh_port"]
        name = server["name"]
        days_difference = 5
        chanel_id = server["company__chanel_id"]
        if not is_server_alive(ipv4):

            alert = Alert.objects.filter(server_id=id)
            if alert.exists():
                alert = alert.first()
                if (now() - alert.time).days > days_difference:
                    send_alert_with_file(
                        chat_id=chanel_id,
                        server_ip=ipv4,
                        service_name=f"{name} server has not been restored for 5 days",
                        id=id,
                    )
                    alert.time = now()
                    alert.save()
            else:
                alert = Alert.objects.create(server_id=id, time=now())
                send_alert_with_file(
                    chat_id=chanel_id, server_ip=ipv4, service_name="Server is " + name
                )
            continue

        applications = Application.objects.filter(server_id=id).values(
            "id", "name_run_on_server", "port"
        )

        for application in applications:
            app_id = application["id"]
            run_name = application["name_run_on_server"]
            port = application["port"]

            if not is_port_open(ip=ipv4, port=port):

                ssh = ssh_connect(ipv4, username, password, ssh_port)

                if ssh:

                    docker_data = get_docker_ports_via_ssh(ssh).values()
                    ports = []
                    for port_item in docker_data:
                        ports += list(port_item.keys())

                    if port in ports:
                        continue

                    logs = get_logs(ssh, run_name)
                    ssh.close()
                else:
                    logs = ""

                alert = Alert.objects.filter(application_id=app_id)
                if alert.exists():
                    alert = alert.first()
                    if (now() - alert.time).days > days_difference:

                        send_alert_with_file(
                            chat_id=chanel_id,
                            server_ip=ipv4,
                            service_name=run_name,
                            logs=logs,
                            port=port,
                            id=id,
                        )
                        alert.time = now()
                else:
                    alert = Alert.objects.create(application_id=app_id, time=now())
                    send_alert_with_file(
                        chat_id=chanel_id,
                        server_ip=ipv4,
                        service_name=run_name,
                        logs=logs,
                        port=port,
                        id=id,
                    )


@app.task
def check_domain_ssl():
    domains = Domain.objects.all().values(
        "id", "domain", "company__chanel_id", "server__id"
    )
    for domain in domains:
        id = domain["server__id"]
        domain_name = domain["domain"]
        chanel_id = domain["company__chanel_id"]

        result = check_ssl_certificate(domain_name)

        if result["is_valid"]:
            if (result["valid_to"] - datetime.now()).days < 0:
                message = (
                    f"<b>Domain:</b> {domain_name}\n"
                    f"<b>Status:</b> SSL certificate validity period has expired\n"
                    f"https://{settings.DOMAIN}/apps/{id}"
                )
                alert = Alert.objects.filter(domain_id=id)
                if not alert.exists():
                    Alert.objects.create(domain_id=id, time=now())
                    send_ssl_status(message)

                elif (alert.exists() and now() - alert.first().time).days > 5:
                    alert = alert.first()
                    alert.time = now()
                    alert.save()
                    send_ssl_status(message)

            if (result["valid_to"] - datetime.now()).days < 6:

                message = (
                    f"<b>Domain:</b> {domain_name}\n"
                    f"<b>Status:</b> SSL certificate validity period has expired\n"
                    f"<b>Days remaining until certificate expiration:</b> {(result['valid_to'] - datetime.now()).days}"
                    f"https://{host_name}/apps/{id}"
                )
                alert = Alert.objects.filter(domain_id=id)
                if not alert.exists():
                    Alert.objects.create(domain_id=id, time=now())
                    send_ssl_status(message)

                elif (alert.exists() and now() - alert.first().time).days > 5:
                    alert = alert.first()
                    alert.time = now()
                    alert.save()
                    send_ssl_status(message, chanel_id)

        else:
            message = (
                f"<b>Domain:</b> {domain_name}\n"
                f"<b>Status:</b> SSL certificate validity period has expired\n"
            )

            alert = Alert.objects.filter(domain_id=id)
            if not alert.exists():
                Alert.objects.create(domain_id=id, time=now())
                send_ssl_status(message, chanel_id)

            elif (alert.exists() and now() - alert.first().time).days > 5:
                alert = alert.first()
                alert.time = now()
                alert.save()
                send_ssl_status(message, chanel_id)


@app.task
def check_docker_app():
    servers = (
        Server.objects.all()
        .select_related("company")
        .values(
            "id",
            "name",
            "ipv4",
            "username",
            "password",
            "ssh_port",
            "company__chanel_id",
        )
    )

    for server in servers:
        
        id = server["id"]
        ipv4 = server["ipv4"]
        username = server["username"]
        password = server["password"]
        ssh_port = server["ssh_port"]
        name = server["name"]
        days_difference = 5
        chanel_id = server["company__chanel_id"]
        
        if not is_server_alive(ipv4):

            alert = Alert.objects.filter(server_id=id)
            if alert.exists():
                alert = alert.first()
                if (now() - alert.time).days > days_difference:
                    send_alert_with_file(
                        chat_id=chanel_id,
                        server_ip=ipv4,
                        service_name=f"{name} server has not been restored for 5 days",
                        id=id,
                    )
                    alert.time = now()
                    alert.save()
            else:
                alert = Alert.objects.create(server_id=id, time=now())
                send_alert_with_file(
                    chat_id=chanel_id, server_ip=ipv4, service_name="Server is " + name
                )
            continue

        applications = DockerApplication.objects.filter(server_id=id).values(
            "id", "name_run_on_docker", "port" , "container_name"
        )

        ssh = ssh_connect(ipv4, username, password, ssh_port)

        for application in applications:
            app_id = application["id"]
            container_name = application
            run_name = application["name_run_on_docker"]
            container_name = application["container_name"]
            port = application["port"]

            if not is_inner_port(ssh, port):

                if ssh:

                    docker_data = get_logs_and_performance_by_port(ssh, container_name, port)
                    
                    image_name = docker_data['image_name']
                    logs = docker_data['recent_logs']
                
                else:
                    logs = ""
                    image_name = ''

                alert = Alert.objects.filter(docker_id=app_id)
                if alert.exists():
                    alert = alert.first()
                    if (now() - alert.time).days > days_difference:

                        send_alert_with_file(
                            chat_id=chanel_id,
                            server_ip=ipv4,
                            service_name=image_name or container_name,
                            logs=logs,
                            port=port,
                            id=id,
                        )
                        alert.time = now()
                else:
                    alert = Alert.objects.create(docker_id=app_id, time=now())
                    send_alert_with_file(
                        chat_id=chanel_id,
                        server_ip=ipv4,
                        service_name=run_name,
                        logs=logs,
                        port=port,
                        id=id,
                    )
        ssh.close()

