import os, telegram
from telegram.ext import Updater, CommandHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("MY_CHAT_ID")

updater = Updater(token=TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", lambda u,c: u.message.reply_text("ربات فعال است")))
updater.start_polling()
updater.idle()
