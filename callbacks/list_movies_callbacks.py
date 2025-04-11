from telegram import ReplyKeyboardMarkup

from admin import send_movie_page
from buttons import buttons_for_admin
from telegram.ext import ConversationHandler

async def handle_pagination(update, context):
    query = update.callback_query
    await query.answer()

    action, current_page = query.data.split("_")
    current_page = int(current_page)

    if action == "next":
        context.user_data["page"] = current_page + 1
    elif action == "prev":
        context.user_data["page"] = current_page - 1
        if context.user_data["page"] < 0:
            context.user_data["page"] = 0
    elif action == "exit":
        await query.edit_message_text("Bosh ADMIN menyu:", reply_markup=ReplyKeyboardMarkup(buttons_for_admin))
        return ConversationHandler.END


    return await send_movie_page(update, context)