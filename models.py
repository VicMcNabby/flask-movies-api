import sqlite3


def drop_table():
    with sqlite3.connect('movies.db') as connection:
        c = connection.cursor()
        c.execute("""DROP TABLE IF EXISTS movies;""")
    return True


def create_db():
    with sqlite3.connect('movies.db') as connection:
        c = connection.cursor()
        table = """CREATE TABLE movies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_actor TEXT NOT NULL,
            title TEXT NOT NULL,
            tagline TEXT NOT NULL
        );
        """
        c.execute(table)
    return True


if __name__ == '__main__':
    drop_table()
    create_db()
