import paramiko


# SSH orqali ulanish
def ssh_connect(ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
        return ssh
    except Exception as e:
        print(f"{ip} serveriga ulanishda xatolik: {e}")
        return None