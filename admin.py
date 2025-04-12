from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler
from config import *
from database.database_movies import DATABASE
from buttons import buttons_for_admin, back

db = DATABASE("database/movies.db")

ADD_MOVIE, ADD_GENRE, ADD_YEAR, ADD_COUNTRY, ADD_CODE, UPLOAD_MOVIE = range(6)
UPDATE, CHECK_CODE, UPDATE_GENRE, UPDATE_YEAR, UPDATE_COUNTRY, UPDATE_MOVIE = range(6)

async def admin_menu(update, context):
    if update.effective_user.id == ADMIN:
        await update.message.reply_text(
            "Xush kelibsiz, admin! 👋\nMarhamat, bo'limni tanlang (bo'limdan chiqish uchun /stop ni bosing):",
            reply_markup=ReplyKeyboardMarkup(buttons_for_admin, resize_keyboard=True)
        )

""" ---------------------- ADD NEW MOVIE ---------------------- """
async def add_movie(update, context):
    await update.message.reply_text(
        "Kino nomini kiriting: 🎬",
        reply_markup=ReplyKeyboardRemove()
    )
    return ADD_MOVIE


async def add_genre(update, context):
    movie_name = update.message.text
    context.user_data["movie_name"] = movie_name
    await update.message.reply_text("Kino janrini kiriting:")
    return ADD_GENRE

async def add_year(update, context):
    movie_genre = update.message.text
    context.user_data["movie_genre"] = movie_genre
    await update.message.reply_text("Kino yilini kiriting:")
    return ADD_YEAR

async def add_country(update, context):
    movie_year = update.message.text
    try:
        movie_year = int(movie_year)  # yoki float(movie_year) agar kerak bo‘lsa
    except ValueError:
        await update.message.reply_text("Iltimos, faqat raqam kiriting (masalan: 2020):")
        return ADD_YEAR
    context.user_data["movie_year"] = movie_year
    await update.message.reply_text("Kino davlatini kiriting:")
    return ADD_COUNTRY

async def add_code(update, context):
    movie_country = update.message.text
    context.user_data["movie_country"] = movie_country
    await update.message.reply_text("Kino kodini kiriting: ")
    return ADD_CODE

async def ask_for_movie(update, context):
    movie_code = update.message.text
    try:
        movie_code = int(movie_code)
    except ValueError:
        await update.message.reply_text("Iltimos, faqat raqam kiriting (masalan: 15):")
        return ADD_CODE

    if db.check_movie_code(movie_code):
        await update.message.reply_text("Bu kodda kino mavjud, iltimos boshqa kod kiriting:")
        return ADD_CODE

    context.user_data["movie_code"] = movie_code
    await update.message.reply_text(f"Kino kodi qabul qilindi: {movie_code}\nEndi filmini yuboring 🎥")
    return UPLOAD_MOVIE

async def save_movie_file(update, context):
    try:
        movie_name = context.user_data.get("movie_name")
        movie_genre = context.user_data.get("movie_genre")
        movie_year = context.user_data.get("movie_year")
        movie_country = context.user_data.get("movie_country")
        movie_code = int(context.user_data.get("movie_code"))
        movie_file = update.message.video

        if not movie_file:
            await update.message.reply_text(
                "❌ Kino fayli topilmadi. Iltimos, video fayl yuboring! 🎥"
            )
            return UPLOAD_MOVIE

        file_id = movie_file.file_id

        result = db.set_movie(movie_name, movie_code, int(movie_year), movie_genre, movie_country, file_id, 0)
        await update.message.reply_text(
            f"{result}\n✅ Kino muvaffaqiyatli qo'shildi!",
            reply_markup=ReplyKeyboardMarkup(buttons_for_admin, resize_keyboard=True)
        )
        return ConversationHandler.END

    except Exception as e:
        await update.message.reply_text(
            f"❌ Xatolik yuz berdi: {e}\nIltimos, qayta urinib ko'ring."
        )
        return UPLOAD_MOVIE


""" ---------------------- UPDATE MOVIE ---------------------- """
async def update(update, context):
    await update.message.reply_text(
        "Tahrirlanadigan kino kodini kiriting: 🔄",
        reply_markup=ReplyKeyboardRemove()
    )
    return UPDATE

async def check_code(update, context):
    movie_code_input = update.message.text

    try:
        movie_code = int(movie_code_input)
    except ValueError:
        await update.message.reply_text(
            "❌ Iltimos faqat raqam kiriting: masalan, 123."
        )
        return UPDATE
    context.user_data["movie_code"] = movie_code
    result = db.check_movie_code(movie_code)

    if result:
        await update.message.reply_text("Kino nomini kiriting: 📝")
        return CHECK_CODE
    else:
        await update.message.reply_text(
            "❌ Bu koddagi kino topilmadi. Iltimos, boshqa kodni kiriting.",
            reply_markup=ReplyKeyboardMarkup(buttons_for_admin, resize_keyboard=True)
        )
        return ConversationHandler.END

async def update_genre(update, context):
    update_name = update.message.text
    context.user_data["update_name"] = update_name
    await update.message.reply_text("Janrni kiriting:")
    return UPDATE_GENRE

async def update_year(update, context):
    update_genre = update.message.text
    context.user_data["update_genre"] = update_genre
    await update.message.reply_text("Yilini kiriting:")
    return UPDATE_YEAR

async def update_country(update, context):
    update_year = update.message.text
    if update_year != "." and not update_year.isdigit():
        await update.message.reply_text("Iltimos faqat son yoki '.' kiriting:")
        return UPDATE_YEAR
    context.user_data["update_year"] = update_year
    await update.message.reply_text("Davlatini kiriting:")
    return UPDATE_COUNTRY

async def update_movie(update, context):
    update_country = update.message.text
    context.user_data["update_country"] = update_country
    await update.message.reply_text("Yangi kinoni yuboring:")
    return UPDATE_MOVIE

async def save_update(update, context):
    movie_code = int(context.user_data["movie_code"])
    update_name = context.user_data["update_name"]
    update_genre = context.user_data["update_genre"]
    update_year = context.user_data["update_year"]
    update_country = context.user_data["update_country"]

    if update.message.video:
        try:
            movie_file = update.message.video
            if not movie_file:
                await update.message.reply_text(
                    "❌ Kino fayli topilmadi. Iltimos, video fayl yuboring! 🎬"
                )
                return UPDATE_MOVIE

            file_id = movie_file.file_id
            db.update_item("movie_id", str(file_id), movie_code)

            if update_name != ".":
                db.update_item("movie_name", update_name, movie_code)
            if update_genre != ".":
                db.update_item("genre", update_genre, movie_code)
            if update_year != ".":
                db.update_item("year", update_year, movie_code)
            if update_country != ".":
                db.update_item("country", update_country, movie_code)

            await update.message.reply_text("✅ Kino muvaffaqiyatli yangilandi!")
            return ConversationHandler.END

        except Exception as e:
            await update.message.reply_text(
                f"❌ Xatolik yuz berdi. Iltimos qayta urining: {e}"
            )
            return UPDATE_MOVIE
    elif update.message.text and update.message.text == ".":
        if update_name != ".":
            db.update_item("movie_name", update_name, movie_code)
        if update_genre != ".":
            db.update_item("genre", update_genre, movie_code)
        if update_year != ".":
            db.update_item("year", update_year, movie_code)
        if update_country != ".":
            db.update_item("country", update_country, movie_code)
        await update.message.reply_text("✅ Kino ma'lumotlari muvaffaqiyatli yangilandi!")
        return ConversationHandler.END

    else:
        await update.message.reply_text(
            "❌ Noto'g'ri format! Kino videosini yoki '.' belgisi yuboring."
        )
        return UPDATE_MOVIE


""" ---------------------- DELETE MOVIE ---------------------- """
async def get_code(update, context):
    await update.message.reply_text(
        "O'chiriladigan kino kodini kiriting: 🗑️"
    )
    return 0

async def delete_movie(update, context):
    delete_movie_code = update.message.text

    try:
        delete_movie_code = int(delete_movie_code)
    except ValueError:
        await update.message.reply_text(
            "❌ Iltimos faqat son yuboring: masalan, 123"
        )
        return 0

    result = db.check_movie_code(delete_movie_code)

    if result:
        del_msg = db.delete_item(delete_movie_code)
        await update.message.reply_text(f"✅ {del_msg}")
    else:
        await update.message.reply_text(
            "❌ Bu kodda kino mavjud emas. Iltimos, boshqa kodni kiriting."
        )
    return ConversationHandler.END

""" ---------------------- GET MOVIE ---------------------- """
async def ask_how_many(update, context):
    await update.message.reply_text(
        "Nechta kinoni ko‘rmoqchisiz? 🎥", reply_markup=ReplyKeyboardRemove()
    )
    return 1

async def send_movie_page(update, context):
    count = context.user_data['count']
    page = context.user_data['page']
    offset = page * count

    movies = db.get_movies(count, offset)
    if not movies:
        await update.message.reply_text("❌ Kino topilmadi.")
        return ConversationHandler.END

    text = "\n\n".join([f"{i+1+offset}. {movie['movie_name']}" for i, movie in enumerate(movies)])

    keyboard = []
    if page > 0:
        keyboard.append([InlineKeyboardButton("⬅️ Oldingi", callback_data=f"prev_{page}")])
    if len(movies) == count:
        keyboard.append([InlineKeyboardButton("Keyingi ➡️", callback_data=f"next_{page}")])
        keyboard.append([InlineKeyboardButton("Chiqish", callback_data="exit_0")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

    return 1

async def show_movies(update, context):
    try:
        count = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Iltimos faqat son kiriting:")
        return 1
    context.user_data['count'] = count
    context.user_data['page'] = 0
    return await send_movie_page(update, context)

