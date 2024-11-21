import requests

def send_alert_with_file(server_ip, port, service_name, logs, file_path):
    telegram_token = "7846581361:AAHWEXIAr0-BFfUrYHSjFzWLLRZOIi6CNvo"
    chat_id = "-1002351022392"

    # Xabar matni
    message = (
        f"Ogohlantirish:\n"
        f"Server: {server_ip}\n"
        f"Port: {port}\n"
        f"Xizmat: {service_name} ishlamayapti!\n\n"
        f"Oxirgi loglar:\n{logs}"
    )

    # Xabarni yuborish
    send_message_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    response = requests.post(send_message_url, data={"chat_id": chat_id, "text": message})

    if response.status_code == 200:
        print("Xabar muvaffaqiyatli yuborildi.")
    else:
        print("Xabar yuborishda xatolik:", response.text)

    # Faylni yuborish
    send_file_url = f"https://api.telegram.org/bot{telegram_token}/sendDocument"
    with open(file_path, 'rb') as file:
        files = {'document': file}
        data = {"chat_id": chat_id, "caption": "Ogohlantirish fayli ilova qilindi."}
        file_response = requests.post(send_file_url, data=data, files=files)

    if file_response.status_code == 200:
        print("Fayl muvaffaqiyatli yuborildi.")
    else:
        print("Fayl yuborishda xatolik:", file_response.text)

# Test qilish
send_alert_with_file("126.16", "54555", "Service Name", "logs", "check_server/test_file.txt")
