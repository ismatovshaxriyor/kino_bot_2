from telegram import ReplyKeyboardMarkup
from buttons import main_menu
import logging

async def start_handler(update, context):
    await update.message.reply_text(text=f"Salom {update.effective_user.first_name}\nKino botga xush kelibsiz\nMarhamat bo'limni tanlang:", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True, one_time_keyboard=True))

# async def false_command(update, context):
#     await update.message.reply_text("Noto'g'ri buyruq")

async def error_handler(update, context):
    logging.error(f"Error {update} caused by {context.error}")