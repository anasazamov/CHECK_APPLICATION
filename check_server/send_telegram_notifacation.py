import requests
import os
from django.conf import settings

host_name = settings.DOMAIN

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
send_message_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"


def send_alert_with_file(
    chat_id, server_ip, service_name, id, logs="", port="The server is down"
):

    chat_id = "-100" + chat_id
    message = (
        f"<b>Red Alert:</b>\n"
        f"<b>Server:</b> {server_ip}\n"
        f"<b>Port:</b> {port}\n"
        f"<b>Service:</b> {service_name} is not working!\n"
        f"{host_name}/apps/{id}"
    )

    (
        requests.post(
            send_message_url,
            data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"},
        ).text
    )

    send_file_url = f"https://api.telegram.org/bot{telegram_token}/sendDocument"

    if logs:
        with open("logs.txt", "w") as f:
            f.write("Logs\n" + logs)

        with open("logs.txt", "rb") as file:
            files = {"document": file}
            data = {"chat_id": chat_id, "caption": "Warning file attached"}
            file_response = requests.post(send_file_url, data=data, files=files)
            os.remove("logs.txt")


def send_ssl_status(message, chat_id):
    chat_id = "-100" + chat_id
    requests.post(
        send_message_url.format(telegram_token),
        data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"},
    )


def get_chat_info(chat_id):
    chat_id = "-100" + str(chat_id)
    url = f"https://api.telegram.org/bot{telegram_token}/getChat"
    params = {"chat_id": chat_id}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        chat_data = response.json()
        if chat_data["ok"]:
            result = chat_data["result"]
            return {
                "chat_name": result.get("title", ""),
                "chat_type": result.get("type", ""),
                "username": result.get("username", ""),
                "description": result.get("description", ""),
            }
        else:
            return {"error": chat_data["description"], "success": True}
    else:
        return {
            "error": f"Xatolik yuz berdi: {response.status_code}, {response.text}",
            "success": False,
        }
