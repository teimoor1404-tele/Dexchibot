import os, json, threading
from flask import Flask
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = int(os.environ.get("MY_CHAT_ID", 0))

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

def save_wallet(addr, cluster, weight):
    try:
        data = json.load(open("wallets.json"))
    except:
        data = []
    data.append({"addr": addr, "cluster": cluster, "weight": weight})
    json.dump(data, open("wallets.json", "w"))

def start_bot():
    bot = Bot(token=TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    
    def cmd_start(update, context):
        kb = [
            [InlineKeyboardButton("🔥 Cluster A", callback_data="c_a"),
             InlineKeyboardButton("⚡ Cluster B", callback_data="c_b")],
            [InlineKeyboardButton("💎 High Win", callback_data="c_h"),
             InlineKeyboardButton("👤 Solo Trader", callback_data="c_s")]
        ]
        update.message.reply_text("کدام کلاستر؟", reply_markup=InlineKeyboardMarkup(kb))
    
    def btn_click(update, context):
        q = update.callback_query
        q.answer()
        q.edit_message_text(f"انتخاب شد: {q.data}\nحالا آدرس کیف را بفرست.")
        context.user_data["sel"] = q.data
    
    def msg_text(update, context):
        if "sel" in context.user_data:
            save_wallet(update.message.text, context.user_data["sel"], 2)
            update.message.reply_text("✅ ذخیره شد. از GMGN/Birdeye تأیید کن.")
            del context.user_data["sel"]
        else:
            update.message.reply_text("ابتدا /start بزن.")
    
    dp.add_handler(CommandHandler("start", cmd_start))
    dp.add_handler(CallbackQueryHandler(btn_click))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, msg_text))
    updater.start_polling()
    updater.idle()

threading.Thread(target=start_bot, daemon=True).start()
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
