import os
import socket
import ssl
from datetime import datetime

# Serverning ping orqali holatini tekshirish
import subprocess
import platform

def is_server_alive(ip):
    # Platformaga qarab parametrni tanlash
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        subprocess.run(
            ["ping", param, "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

# Portning holatini tekshirish
def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            return result == 0
    except Exception as e:
        # print(f"Port {port}ni tekshirishda xatolik: {e}")
        return False


def check_ssl_certificate_via_ssh(ssh, ip, username, password, domain, port=443):
    if not ssh:
        return {"error": f"{ip} serveriga ulanishda xatolik"}

    try:
        # Sertifikatni tekshirish
        context = ssl.create_default_context()
        with socket.create_connection((domain, port)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssl_sock:
                cert = ssl_sock.getpeercert()

        # Sertifikat ma'lumotlari
        issuer = dict(x[0] for x in cert['issuer'])
        issued_to = dict(x[0] for x in cert['subject'])['commonName']
        valid_from = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
        valid_until = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')

        # Sertifikat haqida ma'lumotni qaytarish
        return {
            "Server": ip,
            "Domain": domain,
            "Issued To": issued_to,
            "Issuer": issuer['organizationName'],
            "Valid From": valid_from,
            "Valid Until": valid_until,
            "Is Valid": datetime.now() < valid_until
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        ssh.close()


# print(is_server_alive("51.250.22.154"))
# print(is_port_open("127.0.0.1",80))