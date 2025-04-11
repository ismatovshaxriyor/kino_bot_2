import sqlite3
from contextlib import closing

class DATABASE:
    def __init__(self, db_name):
        self.db_name = db_name

    def get_connection(self):
        return closing(sqlite3.connect(self.db_name))

    def check_movie_code(self, movie_code):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM movies WHERE movie_code = ? LIMIT 1", (movie_code,))
                ans = cursor.fetchone()
            return ans is not None
        except Exception as e:
            return f"Ma'lumot olishda xatolik: {e}"

    """ ------------------- FOR ADMIN'S CONTROL ------------------- """

    def set_movie(self, movie_name, movie_code, year, genre, country, movie_id, rating):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                sql = "INSERT INTO movies (movie_name, movie_code, year, genre, country, movie_id, rating) VALUES (?, ?, ?, ?, ?, ?, ?)"
                val = (movie_name, movie_code, year, genre, country, movie_id, rating)
                cursor.execute(sql, val)
                conn.commit()
            return "Malumotlar saqlandi"
        except Exception as e:
            return f"Malumnot saqlashda xatolik: {e}"

    def delete_item(self, movie_code):
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM movies WHERE movie_code = ?", (movie_code,))
                connection.commit()
            return "Ma'lumot o'chirildi"
        except Exception as e:
            return f"Ma'lumot o'chirilmadi: {e}"

    def update_item(self, column_name, value, movie_code):
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(f"UPDATE movies SET {column_name} = ? WHERE movie_code = ?", (value, movie_code))
                connection.commit()
        except Exception as e:
            print(f'Ma\'lumotlar yangilanmadi: {e}')

    def get_movies(self, count=50, offset=0):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT movie_name, movie_code FROM movies LIMIT {count} OFFSET {offset}")
                rows = cursor.fetchall()
                return [{"movie_name": r[0], "movie_code": r[1]} for r in rows]
        except Exception as e:
            print(e)

    """ ------------------- FOR USERS ------------------- """
    def get_movie_by_code(self, movie_code):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT movie_name, year, genre, country, movie_id, rating FROM movies WHERE movie_code = ?", (movie_code,))
                ans = cursor.fetchone()
                cursor.execute(f"UPDATE movies SET rating = ? WHERE movie_code = ?", (ans[5] + 1, movie_code))
                conn.commit()
            return ans[0], ans[1], ans[2], ans[3], ans[4], ans[5] + 1
        except Exception as e:
            return f"Ma'lumot olishda xatolik: {e}"

    def get_genres(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT genre FROM movies")
            rows = cursor.fetchall()

            unique_genres = set()

            for row in rows:
                if row[0]:
                    genres = row[0].split(",")
                    for genre in genres:
                        unique_genres.add(genre.strip())

            sorted_genres = sorted(unique_genres)
            return sorted_genres

    def get_movies_by_genres(self, genre):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT movie_name, movie_code FROM movies WHERE genre LIKE ?", (f"%{genre}%",))
            ans = cursor.fetchall()
            if ans is None:
                raise ValueError("fetchall() None qaytardi, ma’lumotlar bazasi bilan muammo bor.")

            data = []
            for movie_name, movie_code in ans:
                data.append([movie_name, movie_code])

            return data

    def get_years(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT year FROM movies")
            ans = cursor.fetchall()

            unique_years = set()

            for i in ans:
                unique_years.add(i[0])

            sorted_years = sorted(unique_years)
            return sorted_years

    def get_movies_by_years(self, year):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT movie_name, movie_code FROM movies WHERE year = ?", (year,))
            ans = cursor.fetchall()

            if ans is None:
                raise ValueError("fetchall() None qaytardi, ma’lumotlar bazasi bilan muammo bor.")

            data = []
            for movie_name, movie_code in ans:
                data.append([movie_name, movie_code])

            return data

    def get_movies_by_name(self, movie_name):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT year, genre, country, movie_id, rating FROM movies WHERE movie_name = ?", (movie_name,))
                ans = cursor.fetchone()
                cursor.execute("UPDATE movies SET rating = ? WHERE movie_name = ?", (ans[4] + 1, movie_name))
                conn.commit()
                return ans[0], ans[1], ans[2], ans[3], ans[4] + 1
        except:
            return "Kino topilmadi"

