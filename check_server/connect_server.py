import paramiko

# connect via SHH
def ssh_connect(ip, username, password, port):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password, port=port)
        return ssh
    except Exception as e:
        return None


def get_performance(ssh: paramiko.SSHClient):

    performance_data = {}

    try:
        # CPU
        stdin, stdout, stderr = ssh.exec_command(
            "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'"
        )
        cpu_usage = stdout.read().decode().strip()
        performance_data["cpu_usage"] = f"{cpu_usage}%"

        # RAM
        stdin, stdout, stderr = ssh.exec_command(
            "free -h | awk '/Mem:/ {print $3 \"/\" $2}'"
        )
        ram_usage = stdout.read().decode().strip()
        performance_data["ram_usage"] = ram_usage

        # Disk
        stdin, stdout, stderr = ssh.exec_command(
            "df -h --total | grep 'total' | awk '{print $3 \"/\" $2}'"
        )
        disk_usage = stdout.read().decode().strip()
        performance_data["disk_usage"] = disk_usage

        # Tarmoq (opsiyonal)
        stdin, stdout, stderr = ssh.exec_command(
            "ifstat -i eth0 1 1 | awk 'NR==4 {print $1 \" kB/s\"}'"
        )
        network_usage = stdout.read().decode().strip()
        performance_data["network_usage"] = network_usage
    except Exception as e:
        performance_data = {
            "cpu_usage": "",
            "disk_usage": "",
            "network_usage": "",
            "ram_usage": "",
        }

    return performance_data



ssh = ssh_connect("127.0.0.1", "linux", "242000", 22)

