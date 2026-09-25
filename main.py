import os, json
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

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

@app.route(f"/hook/{TOKEN}", methods=["POST","GET"])
def hook():
    if request.method=="GET":
        bot.set_webhook(url=f"https://dexchibot.onrender.com/hook/{TOKEN}")
        return "Webhook set"
    update = Update.de_json(request.get_json(force=True), bot)
    dp = Dispatcher(bot, None, workers=0, use_context=True)
    
    def start(u,c):
        kb=[[InlineKeyboardButton("🔥 A",callback_data="a"),InlineKeyboardButton("⚡ B",callback_data="b")],
            [InlineKeyboardButton("💎 HighWin",callback_data="h"),InlineKeyboardButton("👤 Solo",callback_data="s")]]
        bot.send_message(chat_id=u.message.chat_id, text="کلاستر:", reply_markup=InlineKeyboardMarkup(kb))
    
    def btn(u,c):
        q=u.callback_query; q.answer()
        c.user_data["sel"]=q.data
        bot.send_message(chat_id=CHAT_ID,text=f"انتخاب: {q.data}\nحالا آدرس کیف را بفرست.")
    
    def msg(u,c):
        if "sel" in c.user_data:
            save(u.message.text, c.user_data["sel"], 2)
            bot.send_message(chat_id=CHAT_ID, text=f"✅ ذخیره شد: {u.message.text}")
            del c.user_data["sel"]
        else:
            bot.send_message(chat_id=CHAT_ID, text="ابتدا /start بزن.")
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(btn))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, msg))
    dp.process_update(update)
    return "ok"

if __name__=="__main__":
    bot.set_webhook(url=f"https://dexchibot.onrender.com/hook/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
