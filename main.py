import os
from flask import Flask
from telegram import Bot
import threading

app = Flask(__name__)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("MY_CHAT_ID")
bot = Bot(token=TOKEN)

@app.route("/")
def health():
    return "OK", 200

def start():
    try:
        bot.send_message(chat_id=CHAT_ID, text="ربات روی رندر فعال شد")
    except:
        pass

if __name__ == "__main__":
    threading.Thread(target=start, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
