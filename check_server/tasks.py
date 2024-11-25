from core.celery import app
from datetime import datetime
from .get_log import get_logs
from django.utils.timezone import now
from .connect_server import ssh_connect
from .models import Server, Application, Alert, Domain, Company
from .send_telegram_notifacation import send_alert_with_file, send_ssl_status
from .check_functions import (
    is_server_alive,
    is_port_open, 
    check_ssl_certificate
)

@app.task
def manitor_server():
    servers = Server.objects.all().select_related("company").values("id","name","ipv4", "username", "password", "ssh_port", "company__chanel_id")

    for server in servers:
        id = server["id"]
        ipv4 = server["ipv4"]
        username = server["username"]
        pasword = server["password"]
        ssh_port = server["ssh_port"]
        name = server["name"]
        days_difference = 5
        chanel_id = server['company__chanel_id']
        print(chanel_id)
        # print(f"{ipv4} {is_server_alive(ipv4)}")
        if not is_server_alive(ipv4):
            
            alert = Alert.objects.filter(server_id=id)
            if alert.exists():
                alert = alert.first()
                if (now() - alert.time).days > days_difference:
                    send_alert_with_file(chat_id=chanel_id, server_ip=ipv4, service_name=f"{name} server has not been restored for 5 days")
                    alert.time = now()
                    alert.save()
            else:
                alert = Alert.objects.create(server_id=id,time=now())
                send_alert_with_file(chat_id=chanel_id, server_ip=ipv4, service_name="Server is "+ name)
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

                        send_alert_with_file(chat_id=chanel_id,server_ip=ipv4, service_name=run_name, logs=logs, port=port)
                        alert.time = now()
                else:
                    alert = Alert.objects.create(application_id=app_id,time=now())
                    send_alert_with_file(chat_id=chanel_id,server_ip=ipv4, service_name=run_name, logs=logs, port=port)


@app.task
def check_domain_ssl():
    domains = Domain.objects.all().values("id", "domain", "company__chanel_id")
    for domain in domains:
        id = domain['id']
        domain_name = domain['domain']
        chanel_id = domain['company__chanel_id']

        result = check_ssl_certificate(domain_name)

        if result['is_valid']:
            if (result['valid_to'] - datetime.now()).days < 0:
                message = (
                        f"<b>Domain:</b> {domain_name}\n"
                        f"<b>Status:</b> SSL certificate validity period has expired\n"                        
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

            if (result['valid_to'] - datetime.now()).days < 6:
               
                message = (
                        f"<b>Domain:</b> {domain_name}\n"
                        f"<b>Status:</b> SSL certificate validity period has expired\n"                        
                        f"<b>Days remaining until certificate expiration:</b> {(result['valid_to'] - datetime.now()).days}"                        
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