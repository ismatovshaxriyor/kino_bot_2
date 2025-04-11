from telegram.ext import ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
from buttons import main_menu

from callbacks.list_genres_callbacks import handle_genres
from callbacks.list_years_callbacks import handle_years

from users import (
    get_movie_by_code, send_movie_by_code,
    get_movie_by_year,
    get_movie_by_genre,
    get_movie_by_name, send_movie_by_name
)

# --------------- BACK ---------------
async def back_menu(update, context):
    await update.message.reply_text("Bosh menyu:", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True, one_time_keyboard=True))
    return ConversationHandler.END

get_code_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(r"^Kod bo'yicha qidirish"), get_movie_by_code)],
    states={
        0: [MessageHandler(filters.Regex(r"^\d+$"), send_movie_by_code)]
    },
    fallbacks=[MessageHandler(filters.Regex("Bosh menyu"), back_menu)],
    per_user=True
)

get_year_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("Yil bo'yicha qidirish"), get_movie_by_year)],
    states={
        0: [CallbackQueryHandler(handle_years, pattern="^(year|exit)_")]
    },
    fallbacks=[MessageHandler(filters.Regex("Bosh menyu"), back_menu)],
    per_user=True
)

get_genre_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("Janr bo'yicha qidirish"), get_movie_by_genre)],
    states={
        0: [CallbackQueryHandler(handle_genres, pattern="^(genre|exit)_")]
    },
    fallbacks=[MessageHandler(filters.Regex("Bosh menyu"), back_menu)],
    per_user=True
)

get_name_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("Nomi bo'yicha qidirish"), get_movie_by_name)],
    states={
        0: [MessageHandler(filters.Regex(r"^(?!.*Bosh menyu).*"), send_movie_by_name)]
    },
    fallbacks=[MessageHandler(filters.Regex("Bosh menyu"), back_menu)],
    per_user=True
)