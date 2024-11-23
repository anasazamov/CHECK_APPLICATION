import socket
import ssl
from datetime import datetime, timedelta

from ping3 import ping

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


import socket
import ssl
from datetime import datetime

def check_ssl_certificate(domain):
    try:

        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssl_sock:

                cert = ssl_sock.getpeercert()

                not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')

                current_time = datetime.utcnow()
                is_valid = not_before <= current_time <= not_after

                return {
                    "domain": domain,
                    "valid_from": not_before,
                    "valid_to": not_after,
                    "is_valid": is_valid,
                }

    except Exception as e:
        return {"domain": domain, "error": str(e), "is_valid": False, "valid_to": datetime.now()-timedelta(days=10)}
