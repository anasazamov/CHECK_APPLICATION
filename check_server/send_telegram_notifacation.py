import requests
import os
telegram_token = "7846581361:AAHWEXIAr0-BFfUrYHSjFzWLLRZOIi6CNvo"
send_message_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

def send_alert_with_file(chat_id, server_ip, service_name, check_id, logs="", port='The server is down'):
    
    chat_id = "-100" + chat_id
    message = (
        f"<b>Red Alert:</b>\n"
        f"<b>Server:</b> {server_ip}\n"
        f"<b>Port:</b> {port}\n"
        f"<b>Service:</b> {service_name} not working!\n"
        f"https://localhost/{check_id}"
    )
    
    requests.post(send_message_url, data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})

    send_file_url = f"https://api.telegram.org/bot{telegram_token}/sendDocument"
    if logs:
        with open("logs.txt", "w") as f:
            f.write("Logs\n" + logs)

        with open("logs.txt", 'rb') as file:
            files = {'document': file}
            data = {"chat_id": chat_id, "caption": "Warning file attached"}
            file_response = requests.post(send_file_url, data=data, files=files)
            os.remove("logs.txt")


def send_ssl_status(message, chat_id):
    chat_id = "-100" + chat_id
    requests.post(
        send_message_url.format(telegram_token),
        data={"chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"})
