import os, json
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN=os.environ.get("TELEGRAM_TOKEN")
CHAT_ID=int(os.environ.get("MY_CHAT_ID",0))
bot=Bot(token=TOKEN)
app=Flask(__name__)

if not os.path.exists("wallets.json"):
    open("wallets.json","w").write("[]")

@app.route("/")
def h(): return "OK"

@app.route(f"/hook/{TOKEN}", methods=["POST"])
def hook():
    j=request.get_json(force=True)
    u=Update.de_json(j,bot) if j else None
    if u and u.message and u.message.text=="/start":
        kb=[[InlineKeyboardButton("🔥 Cluster A","a"),InlineKeyboardButton("⚡ Cluster B","b")],
            [InlineKeyboardButton("💎 High Win","h"),InlineKeyboardButton("👤 Solo Trader","s")]]
        bot.send_message(chat_id=u.message.chat_id,text="انتخاب کن:",reply_markup=InlineKeyboardMarkup(kb))
    elif u and u.callback_query:
        q=u.callback_query; q.answer()
        bot.send_message(chat_id=CHAT_ID,text=f"انتخاب شد: {q.data}\nآدرس کیف را بفرست.")
    elif u and u.message and u.message.text and not u.message.text.startswith("/"):
        bot.send_message(chat_id=CHAT_ID,text=f"✅ ذخیره شد: {u.message.text}")
    return "ok"

if __name__=="__main__":
    bot.set_webhook(url=f"https://dexchibot.onrender.com/hook/{TOKEN}")
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
