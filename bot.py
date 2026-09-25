from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import os

# این دو را بعداً پر می‌کنیم؛ فعلاً خالی بذار
TOKEN = "8815876816:AAHcgXzyr8UL2uLk0e6GudsxRBY11h-GisE"  
MY_CHAT_ID = 233619114

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)

def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🔥 Cluster A", callback_data="cluster_a"),
         InlineKeyboardButton("⚡ Cluster B", callback_data="cluster_b")],
        [InlineKeyboardButton("💎 High Win", callback_data="high_win"),
         InlineKeyboardButton("👤 Solo Trader", callback_data="solo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "کیف پول جدید را اضافه کن. ابتدا دسته‌بندی را انتخاب کن:",
        reply_markup=reply_markup
    )

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
updater.idle()