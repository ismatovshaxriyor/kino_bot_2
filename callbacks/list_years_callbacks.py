from database.database_movies import DATABASE
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup
from buttons import main_menu

db = DATABASE("database/movies.db")

async def handle_years(update, context):
    query = update.callback_query
    data_sp = query.data.split("_")
    await query.answer()

    movies_data = db.get_movies_by_years(int(data_sp[1]))

    if movies_data:
        response = f"{data_sp[1]} yildagi filmlar:\n" + "\n".join(
            [f"{movie[1]} -> {movie[0]}" for movie in movies_data])
    elif data_sp[0] == "exit":
        try:
            await query.message.delete()
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text="Bosh menyu:",
                reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
            )
        except Exception as e:
            print(f"Xabarni o‘chirishda xato: {e}")
            await query.answer("Xabarni o‘chirishda xato yuz berdi.", show_alert=True)
        return ConversationHandler.END
    else:
        response = f"{data_sp[1]} yildagi filmlar topilmadi."


    try:
        await query.message.reply_text(response)
    except Exception as e:
        print(f"xatolik: {e}")