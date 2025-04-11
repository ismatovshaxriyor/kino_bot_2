from telegram.ext import MessageHandler, filters, CommandHandler, CallbackQueryHandler

from admin import *

from buttons import buttons_for_admin

async def back_admin_menu(update, context):
    await update.message.reply_text("Bosh ADMIN menyu:", reply_markup=ReplyKeyboardMarkup(buttons_for_admin, resize_keyboard=True, one_time_keyboard=True))
    return ConversationHandler.END

add_movie_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Kino qo'shish$"), add_movie)],
    states={
        ADD_MOVIE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_genre)],
        ADD_GENRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_year)],
        ADD_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_country)],
        ADD_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_code)],
        ADD_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_movie)],
        UPLOAD_MOVIE: [MessageHandler(filters.VIDEO, save_movie_file)]
    },
    fallbacks=[CommandHandler("stop", back_admin_menu)],
    per_user=True
)

update_movie_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Kinoni tahrirlash$"), update)],
    states={
        UPDATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_code)],
        CHECK_CODE: [MessageHandler(filters.TEXT, update_genre)],
        UPDATE_GENRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_year)],
        UPDATE_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_country)],
        UPDATE_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_movie)],
        UPDATE_MOVIE: [MessageHandler(filters.ALL, save_update)]
    },
    fallbacks=[CommandHandler("stop", back_admin_menu)],
    per_user=True
)

delete_movie_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Kinoni o'chirish$"), get_code)],
        states={
            0: [MessageHandler(filters.TEXT, delete_movie)]
        },
        fallbacks=[CommandHandler("stop", back_admin_menu)],
        per_user=True
)

get_movie_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("Kinolar ro'yxati"), ask_how_many)],
    states={
        1: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, show_movies),
        ]
    },
    fallbacks=[CommandHandler("stop", back_admin_menu)],
    per_user=True,
)