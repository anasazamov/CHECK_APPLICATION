import datetime

def get_logs_by_port(ssh, port):
    find_container_command = (
        f"docker ps --filter 'publish={port}' --format '{{{{.ID}}}}'"
    )
    stdin, stdout, stderr = ssh.exec_command(find_container_command)
    container_id = stdout.read().decode("utf-8").strip()

    if not container_id:
        return ""

    get_logs_command = f"docker logs {container_id}"
    stdin, stdout, stderr = ssh.exec_command(get_logs_command)
    logs = stdout.read().decode("utf-8")
    return logs


def get_logs(ssh, service_name):
    """ """
    try:
        if not service_name.lower() == "docker":
            # Systemd logs
            command = f'journalctl -u {service_name} --since "2 hours ago"'
        else:
            command = f"docker logs"
        stdin, stdout, stderr = ssh.exec_command(command)
        logs = stdout.read().decode("utf-8").strip()
        if not logs:
            return f"Not fund logs for ({service_name})"
        return logs
    except Exception as e:
        return f"Error getting logs: {e}"
    
def get_logs_and_performance_by_port(ssh_client, container_name, internal_port):
    try:
        
        image_command = f"docker inspect --format '{{{{.Config.Image}}}}' {container_name}"
        stdin, stdout, stderr = ssh_client.exec_command(image_command)
        image_name = stdout.read().decode("utf-8").strip()
        
        
        log_command = f"docker logs {container_name}"
        stdin, stdout, stderr = ssh_client.exec_command(log_command)
        logs = stdout.read().decode("utf-8")
        
        
        current_time = datetime.datetime.now()
        two_hours_ago = current_time - datetime.timedelta(hours=2)
        
        
        log_lines = logs.split("\n")
        recent_logs = []
        for line in log_lines:
            try:
        
                log_time_str = line.split(" - - ")[0]
                log_time = datetime.datetime.strptime(log_time_str, "[%d/%b/%Y:%H:%M:%S +0000]")
                
                if log_time >= two_hours_ago:
                    
                    if f":{internal_port}" in line:
                        recent_logs.append(line)
            except Exception as e:
                continue  
        
        recent_logs_str = "\n".join(recent_logs)

        performance_command = f"docker stats --no-stream --format '{{{{.Name}}}}\t{{{{.CPUPerc}}}}\t{{{{.MemUsage}}}}\t{{{{.NetIO}}}}' {container_name}"
        stdin, stdout, stderr = ssh_client.exec_command(performance_command)
        performance = stdout.read().decode("utf-8")
        
        performance_lines = performance.splitlines()
        performance_info = ""
        for line in performance_lines:
            name, cpu, mem, net = line.split("\t")
            performance_info += f"Container: {name}\nCPU Usage: {cpu}\nMemory Usage: {mem}\nNetwork IO: {net}\n\n"
        
        return {
            "image_name": image_name,
            "recent_logs": recent_logs_str,
            "performance": performance_info.strip()
        }
    
    except Exception as e:
        return {'image_name': 'nginx',
                'performance': 
                    ''
                    ''
                    ''
                    '',
                'recent_logs': ''}

from pprint import pprint
    
