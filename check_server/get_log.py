
def get_logs_by_port(ssh, port):
    find_container_command = f"docker ps --filter 'publish={port}' --format '{{{{.ID}}}}'"
    stdin, stdout, stderr = ssh.exec_command(find_container_command)
    container_id = stdout.read().decode("utf-8").strip()

    if not container_id:
        # print(f"Port {port} orqali ishlayotgan konteyner topilmadi.")
        return

    # Loglarni olish
    get_logs_command = f"docker logs {container_id}"
    stdin, stdout, stderr = ssh.exec_command(get_logs_command)
    logs = stdout.read().decode("utf-8")
    return logs
    print(f"Logs for container on port {port}:\n{logs}")

# Xizmat loglarini olish
def get_logs(ssh, service_name):
    try:
        if not service_name.lower() == "docker":
        # Systemd loglari
            command = f'journalctl -u {service_name} --since "2 hours ago"'
        else:
            command = f'docker logs'
        stdin, stdout, stderr = ssh.exec_command(command)
        logs = stdout.read().decode("utf-8").strip()
        if not logs:
            return f"Loglar topilmadi ({service_name})"
        return logs
    except Exception as e:
        return f"Loglarni olishda xatolik: {e}"
