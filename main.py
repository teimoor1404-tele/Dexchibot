import os, json
from flask import Flask
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = int(os.environ.get("MY_CHAT_ID", 0))
bot = Bot(token=TOKEN)
app = Flask(__name__)

if not os.path.exists("wallets.json"):
    open("wallets.json","w").write("[]")

def save(addr, c, w):
    d=json.load(open("wallets.json")); d.append({"w":addr,"c":c,"wgt":w}); json.dump(d, open("wallets.json","w"))

@app.route("/")
def h(): return "OK"

def start_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    def start(u,c):
        kb=[[InlineKeyboardButton("🔥 Cluster A",callback_data="a"),InlineKeyboardButton("⚡ Cluster B",callback_data="b")],
            [InlineKeyboardButton("💎 High Win",callback_data="h"),InlineKeyboardButton("👤 Solo Trader",callback_data="s")]]
        bot.send_message(chat_id=u.message.chat_id, text="کلاستر را انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
    
    def btn(u,c):
        q=u.callback_query; q.answer(); c.user_data["sel"]=q.data
        bot.send_message(chat_id=CHAT_ID, text=f"انتخاب: {q.data}\nآدرس کیف را بفرست.")
    
    def msg(u,c):
        if "sel" in c.user_data:
            save(u.message.text, c.user_data["sel"], 2); bot.send_message(chat_id=CHAT_ID, text=f"✅ ذخیره: {u.message.text}")
            del c.user_data["sel"]
        else:
            bot.send_message(chat_id=CHAT_ID, text="ابتدا /start بزن.")
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(btn))
    dp.add_handler(MessageHandler(lambda u,c: bool(u.message and u.message.text), msg))
    updater.start_polling()
    updater.idle()

import threading
threading.Thread(target=start_bot, daemon=True).start()
app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
