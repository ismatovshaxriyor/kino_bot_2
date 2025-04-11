from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from handlers.common_handlers import start_handler, error_handler
from handlers.for_users_handlers import get_code_conv_handler, get_year_conv_handler, get_genre_conv_handler, get_name_conv_handler
from handlers.for_admin_handlers import add_movie_conv_handler, update_movie_conv_handler, delete_movie_conv_handler, get_movie_conv_handler

from admin import admin_menu
from config import TOKEN

from callbacks.list_movies_callbacks import handle_pagination
from callbacks.list_genres_callbacks import handle_genres

def main():
    bot = Application.builder().token(TOKEN).build()

    # === COMMANDS ===
    bot.add_handler(CommandHandler("start", start_handler))
    bot.add_handler(CommandHandler("admin", admin_menu))

    # === USER HANDLERS ===
    bot.add_handler(get_code_conv_handler)
    bot.add_handler(get_year_conv_handler)
    bot.add_handler(get_genre_conv_handler)
    bot.add_handler(get_name_conv_handler)

    # === ADMIN HANDLERS ===
    bot.add_handler(add_movie_conv_handler)
    bot.add_handler(update_movie_conv_handler)
    bot.add_handler(delete_movie_conv_handler)
    bot.add_handler(get_movie_conv_handler)
    bot.add_handler(CallbackQueryHandler(handle_pagination, pattern=r"^(prev|next|exit)_\d+$"))
    bot.add_handler(CallbackQueryHandler(handle_genres))


    # === OTHER HANDLERS ===
    bot.add_error_handler(error_handler)
    bot.run_polling()

if __name__ == '__main__':
    print("bot started")
    main()
