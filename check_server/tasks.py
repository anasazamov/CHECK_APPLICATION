from core.celery import app
from .get_log import get_logs
from django.utils.timezone import now
from .connect_server import ssh_connect
from .models import Server, Application, Alert
from .send_telegram_notifacation import send_alert_with_file
from .check_functions import (
    is_server_alive,
    is_port_open
)

@app.task
def manitor_server():
    servers = Server.objects.all().values("id","name","ipv4", "username", "password", "ssh_port")

    for server in servers:
        id = server["id"]
        ipv4 = server["ipv4"]
        username = server["username"]
        pasword = server["password"]
        ssh_port = server["ssh_port"]
        name = server["name"]
        days_difference = 5
        # print(f"{ipv4} {is_server_alive(ipv4)}")
        if not is_server_alive(ipv4):
            
            alert = Alert.objects.filter(server_id=id)
            if alert.exists():
                alert = alert.first()
                if (now() - alert.time).days > days_difference:
                    send_alert_with_file(ipv4, "Server is "+name)
                    alert.time = now()
                    alert.save()
            else:
                alert = Alert.objects.create(server_id=id,time=now())
                send_alert_with_file(ipv4, name)
            continue

        applications = Application.objects.filter(server_id=id).values("id","name_run_on_server", "port")

        for application in applications:
            app_id = application['id']
            run_name = application['name_run_on_server']
            port  = application['port']
            

            if not is_port_open(ip=ipv4, port=port):
                ssh = ssh_connect(ipv4, username, pasword, ssh_port)
                logs = get_logs(ssh, run_name)
                ssh.close()
                
                alert = Alert.objects.filter(application_id=app_id)
                if alert.exists():
                    alert = alert.first()
                    if (now() - alert.time).days > days_difference:

                        send_alert_with_file(ipv4, run_name, logs, port)
                        alert.time = now()
                else:
                    alert = Alert.objects.create(application_id=app_id,time=now())
                    send_alert_with_file(ipv4, run_name, logs, port)
