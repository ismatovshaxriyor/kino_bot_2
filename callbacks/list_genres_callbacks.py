from database.database_movies import DATABASE
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup
from buttons import  main_menu

db = DATABASE("database/movies.db")

async def handle_genres(update, context):
    query = update.callback_query
    data_sp = query.data.split("_")
    await query.answer()

    movies_data = db.get_movies_by_genres(data_sp[1])

    if movies_data and data_sp[0] != "exit":
        response = f"{data_sp[1]} janridagi filmlar:\n" + "\n".join(
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

    try:
        if query.message:
            await query.message.reply_text(response)
        else:
            await context.bot.send_message(chat_id=query.from_user.id, text=response)
    except Exception as e:
        print(f"Xatolik: {e}")
        await query.answer("Xatolik yuz berdi.", show_alert=True)