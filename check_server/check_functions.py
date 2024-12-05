import socket
import ssl
from datetime import datetime, timedelta

from ping3 import ping
import json

# from connect_server import ssh_connect


def is_server_alive(ip):
    try:
        response = ping(ip, timeout=1)
        return response is not None
    except Exception:
        return False


def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            return result == 0
    except Exception as e:
        return False


def get_docker_ports_via_ssh(ssh):
    command = "docker ps --format '{{json .}}'"
    stdin, stdout, stderr = ssh.exec_command(command)

    containers_output = stdout.read().decode("utf-8")


    containers = containers_output.splitlines()

    container_ports = {}

    for container in containers:

        container_info = json.loads(container)
        container_name = container_info.get("Names", "").replace("/", "")
        ports = container_info.get("Ports", "")

        if ports:
            port_mapping = {}
            for port_info in ports.split(","):
                port_parts = port_info.split("->")
                if len(port_parts) == 2:
                    external_port = port_parts[1].strip().split("/")[0]
                    internal_port = port_parts[0].strip()
                    service_name = container_info.get("Image", "Unknown service")
                    port_mapping[external_port] = {
                        "internal_port": internal_port,
                        "service": service_name,
                    }
            container_ports[container_name] = port_mapping

    return container_ports


def check_ssl_certificate(domain):
    try:

        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssl_sock:

                cert = ssl_sock.getpeercert()

                not_before = datetime.strptime(
                    cert["notBefore"], "%b %d %H:%M:%S %Y %Z"
                )
                not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")

                current_time = datetime.utcnow()
                is_valid = not_before <= current_time <= not_after

                return {
                    "domain": domain,
                    "valid_from": not_before,
                    "valid_to": not_after,
                    "is_valid": is_valid,
                }

    except Exception as e:
        return {
            "domain": domain,
            "error": str(e),
            "is_valid": False,
            "valid_to": datetime.now(),
        }


def get_open_ports(ssh):
    try:
        stdin, stdout, stderr = ssh.exec_command("netstat -tuln")

        output = stdout.read().decode()

        open_ports = []
        for line in output.splitlines():
            if "LISTEN" in line:
                parts = line.split()
                port = parts[3].split(":")[-1]
                open_ports.append(port)

        return open_ports

    except Exception as e:
        return []


def is_docker_port_active(ssh, port, container_name):
    docker_data = get_docker_ports_via_ssh(ssh).items()
    ports = []
    for key, port_key in docker_data:
        ports += [(item_port, container_name) for item_port in list(port_key.keys())]

    container_colections = (str(port), container_name)
    return container_colections in ports


def get_cainteners(data: dict, target_key: str) -> list:
    parent_keys = []
    for parent_key, nested_data in data.items():
        if target_key in nested_data:
            parent_keys.append(parent_key)
    return parent_keys


# ssh = ssh_connect("127.0.0.1", "linux", "242000", 22)
# from pprint import pprint
# pprint(get_docker_ports_via_ssh((ssh)))
