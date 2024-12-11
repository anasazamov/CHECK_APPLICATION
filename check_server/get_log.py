import datetime

# from connect_server import ssh_connect


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

        image_command = (
            f"docker inspect --format '{{{{.Config.Image}}}}' {container_name}"
        )
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
                log_time = datetime.datetime.strptime(
                    log_time_str, "[%d/%b/%Y:%H:%M:%S +0000]"
                )

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
            "performance": performance_info.strip(),
        }

    except Exception as e:
        return {"image_name": "", "performance": "" "" "" "", "recent_logs": ""}


def check_service_status(ssh_client, service_name: str) -> dict:
    """
    Returns a dictionary containing the status, performance, and recent logs of a service on a remote server.

    Args:
        ssh_client (paramiko.SSHClient): The SSH client object used to execute commands remotely.
        service_name (str): The name of the service to check.

    Returns:
        dict: A dictionary with the status, performance metrics, and recent logs of the service.
    """
    result = {}
    try:
        # Get the status of the service
        status_command = f"systemctl is-active {service_name}"
        stdin, stdout, stderr = ssh_client.exec_command(status_command)
        status = stdout.read().decode().strip()
        if status == "inactive":
            status = "active"

        # Get the performance metrics of the service (CPU and Memory usage)
        performance_command = (
            f"ps aux | grep {service_name} | grep -v grep | awk '{{print $3, $4}}'"
        )
        stdin, stdout, stderr = ssh_client.exec_command(performance_command)
        performance_data = stdout.read().decode().strip()

        if performance_data:
            # Split and process the performance data
            performance_lines = performance_data.split("\n")
            cpu_total = 0.0
            mem_total = 0.0
            process_count = len(performance_lines)

            for line in performance_lines:
                cpu, mem = line.split()
                cpu_total += float(cpu)
                mem_total += float(mem)

            # Calculate average CPU and memory usage
            avg_cpu = cpu_total / process_count if process_count else 0.0
            avg_mem = mem_total / process_count if process_count else 0.0

            performance = f"Average CPU Usage: {avg_cpu:.2f}%\nAverage Memory Usage: {avg_mem:.2f}%"
        else:
            performance = "No performance data available"

        # Get the logs from the last two hours
        current_time = datetime.datetime.now()
        two_hours_ago = current_time - datetime.timedelta(hours=2)
        logs_command = f"journalctl -u {service_name} --since '{two_hours_ago.strftime('%Y-%m-%d %H:%M:%S')}'"
        stdin, stdout, stderr = ssh_client.exec_command(logs_command)
        logs = stdout.read().decode().strip()

        # Handle errors
        error = stderr.read().decode().strip()
        if error:
            raise Exception(f"Error occurred: {error}")

        # Return the result dictionary
        result["status"] = status
        result["performance"] = performance.split("\n")
        result["recent_logs"] = logs if logs else "-- No logs found --"

    except Exception as e:

        result["status"] = ""
        result["performance"] = []
        result["recent_logs"] = ""

    return result


# ssh = ssh_connect("127.0.0.1",'linux', "242000", 22)
# print(check_service_status(ssh,"nginx"))
