import requests
import os

def send_alert_with_file(server_ip, service_name, logs="", port='The server is down'):
    telegram_token = "7846581361:AAHWEXIAr0-BFfUrYHSjFzWLLRZOIi6CNvo"
    chat_id = "-1002351022392"

    # Xabar matni
    message = (
        f"<b>Red Alert:</b>\n"
        f"<b>Server:</b> {server_ip}\n"
        f"<b>Port:</b> {port}\n"
        f"<b>Service:</b> {service_name} not working!"
    )

    # Xabarni yuborish
    send_message_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    response = requests.post(send_message_url, data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})

    # Faylni yuborish
    send_file_url = f"https://api.telegram.org/bot{telegram_token}/sendDocument"
    if logs:
        with open("logs.txt", "w") as f:
            f.write("Logs\n" + logs)

        with open("logs.txt", 'rb') as file:
            files = {'document': file}
            data = {"chat_id": chat_id, "caption": "Warning file attached"}
            file_response = requests.post(send_file_url, data=data, files=files)
            os.remove("logs.txt")

