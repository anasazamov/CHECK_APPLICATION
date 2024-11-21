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