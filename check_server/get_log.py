
def get_logs_by_port(ssh, port):
    find_container_command = f"docker ps --filter 'publish={port}' --format '{{{{.ID}}}}'"
    stdin, stdout, stderr = ssh.exec_command(find_container_command)
    container_id = stdout.read().decode("utf-8").strip()

    if not container_id:
        return

    get_logs_command = f"docker logs {container_id}"
    stdin, stdout, stderr = ssh.exec_command(get_logs_command)
    logs = stdout.read().decode("utf-8")
    return logs
    print(f"Logs for container on port {port}:\n{logs}")

def get_logs(ssh, service_name):
    try:
        if not service_name.lower() == "docker":
        # Systemd logs
            command = f'journalctl -u {service_name} --since "2 hours ago"'
        else:
            command = f'docker logs'
        stdin, stdout, stderr = ssh.exec_command(command)
        logs = stdout.read().decode("utf-8").strip()
        if not logs:
            return f"Not fund logs for ({service_name})"
        return logs
    except Exception as e:
        return f"Error getting logs: {e}"
