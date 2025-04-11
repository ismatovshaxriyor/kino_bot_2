from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from buttons import back
from database.database_movies import DATABASE

db = DATABASE("database/movies.db")

# --------------- SEND MOVIE BY CODE ---------------
async def get_movie_by_code(update, context):
    await update.message.reply_text("Kino kodini yuboring:", reply_markup=ReplyKeyboardMarkup(back))
    return 0

async def send_movie_by_code(update, context):
    movie_code = update.message.text
    try:
        movie_code = int(movie_code)
    except ValueError:
        await update.message.reply_text("Iltimos faqat raqamlarda iborat son yuboring!")
        return 0

    chat_id = update.effective_user.id

    try:
        movie_name, year, genre, country, movie_id, rating = db.get_movie_by_code(movie_code)
        await context.bot.send_video(video=movie_id, chat_id=chat_id, caption=f"Kino nomi: {movie_name}\nJanri: {genre}\nYili: {year}\nDavlati: {country}\nQidiruvlar soni: {rating}")
    except:
        await update.message.reply_text("Bu kodda kino topilmadi.")
    return 0

# --------------- SEND MOVIE BY YEAR ---------------
async def get_year_markup():
    years_list = db.get_years()
    keyboard = []

    if not years_list:
        return InlineKeyboardMarkup([[
            InlineKeyboardButton(text="No genres available", callback_data="no_years")
        ]])

    for i in range(0, len(years_list), 2):
        btn1 = InlineKeyboardButton(text=years_list[i], callback_data=f"year_{years_list[i]}")

        if i + 1 < len(years_list):
            btn2 = InlineKeyboardButton(text=years_list[i + 1], callback_data=f"year_{years_list[i + 1]}")
            keyboard.append([btn1, btn2])
        else:
            keyboard.append([btn1])

    keyboard.append([InlineKeyboardButton(text="Chiqish", callback_data="exit_0")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def get_movie_by_year(update, context):
    markup = await get_year_markup()
    await update.message.reply_text("Kino yilini tanlang: ", reply_markup=markup)
    return 0

# --------------- SEND MOVIE BY GENRE ---------------
def get_genre_markup():
    genres_list = db.get_genres()
    keyboard = []

    if not genres_list:
        return InlineKeyboardMarkup([[
            InlineKeyboardButton(text="No genres available", callback_data="no_genres")
        ]])

    for i in range(0, len(genres_list), 2):
        btn1 = InlineKeyboardButton(text=genres_list[i], callback_data=f"genre_{genres_list[i]}")

        if i + 1 < len(genres_list):
            btn2 = InlineKeyboardButton(text=genres_list[i + 1], callback_data=f"genre_{genres_list[i + 1]}")
            keyboard.append([btn1, btn2])
        else:
            keyboard.append([btn1])

    keyboard.append([InlineKeyboardButton(text="Chiqish", callback_data="exit_0")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def get_movie_by_genre(update, context):
    markup = get_genre_markup()
    await update.message.reply_text("Kino janrini tanlang: ", reply_markup=markup)
    return 0

# --------------- SEND MOVIE BY NAME ---------------
async def get_movie_by_name(update, context):
    await update.message.reply_text("Kino nomini kiriting: ")
    return 0

async def send_movie_by_name(update, context):
    movie_name = update.message.text
    try:
        year, genre, country, movie_id, rating = db.get_movies_by_name(str(movie_name).title())
        await update.message.reply_video(video=movie_id, caption=f"Kino nomi: {str(movie_name).title()}\nYili: {year}\nJanri: {genre}\nDavlati: {country}\nQidirishlar soni: {rating}")
    except:
        err = db.get_movies_by_name(str(movie_name).title())
        await update.message.reply_text(err)
    return 0
