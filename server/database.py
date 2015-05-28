import sqlite3

DATABASE_URI = 'commentary.db'


def connect_db():
    return sqlite3.connect(DATABASE_URI)


# TODO: migrations
def create_default_tables(cursor):
    cursor.execute('''CREATE TABLE comments
                    (id INTEGER PRIMARY KEY NOT NULL,
                    user_id INTEGER NOT NULL,
                    url TEXT NOT NULL,
                    content TEXT NOT NULL)''')


def insert_comment(cursor, comment):
    query = 'INSERT INTO comments (user_id, url, content) VALUES (?, ?, ?)'
    comment_params = (comment.user_id, comment.url, comment.content)
    cursor.execute(query, comment_params)


def get_last_comment(cursor):
    query = 'SELECT * FROM comments ORDER BY id ASC LIMIT 1'
    return cursor.execute(query).fetchone()


def get_comments_for_url(cursor, url):
    query = 'SELECT * FROM comments WHERE url = ? ORDER BY id ASC'
    return cursor.execute(query, (url,)).fetchall()
