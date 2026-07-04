import requests
import time
import os

TOKEN = os.environ["750910516:cNY5hyvY7tAlAU-NrtBox9N3AUfnicMoGX4"]

URL = f"https://tapi.bale.ai/bot{TOKEN}"

ADMIN_CHAT_ID = 813467533

# -----------------------------
# خواندن آخرین پیام ذخیره‌شده
# -----------------------------
if os.path.exists("last_update.txt"):
    with open("last_update.txt", "r") as file:
        last_update = int(file.read())
else:
    last_update = 0

while True:

    response = requests.get(
        f"{URL}/getUpdates",
        params={"offset": last_update + 1}
    ).json()

    if response["ok"]:

        for update in response["result"]:

            update_id = update["update_id"]
            last_update = update_id

            # ذخیره در فایل (حافظه دائمی)
            with open("last_update.txt", "w") as file:
                file.write(str(last_update))

            text = update["message"].get("text", "")
            sender_id = update["message"]["from"]["id"]

            # اگر مدیر بود، رد کن
            if sender_id == ADMIN_CHAT_ID:
                continue

            # ارسال پیام به مدیر
            requests.post(
                f"{URL}/sendMessage",
                json={
                    "chat_id": ADMIN_CHAT_ID,
                    "text": f"📩 سوال جدید\n\n{text}"
                }
            )

            # ارسال پیام تشکر به کاربر
            requests.post(
                f"{URL}/sendMessage",
                json={
                    "chat_id": sender_id,
                    "text": "✅ پیام شما با موفقیت دریافت شد.\n\nپاسخ پس از بررسی ارسال خواهد شد."
                }
            )

            print("پیام پردازش شد ✅")

    time.sleep(2)
