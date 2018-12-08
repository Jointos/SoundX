from flask import Flask, render_template, g,request,redirect,url_for
import sqlite3


tags_sql="""CREATE TABLE IF NOT EXISTS tags(
    sound_id integer NOT NULL,
    name text NOT NULL
);"""

users_sql="""CREATE TABLE IF NOT EXISTS users(
    id integer PRIMARY KEY,
    joined_at DATE NOT NULL,
    nickname text NOT NULL
);"""


sounds_sql=""" CREATE TABLE IF NOT EXISTS sounds(
    id integer PRIMARY KEY,
    name text NOT NULL,
    data blob NOT NULL,
    likes integer NOT NULL,
    dislikes integer NOT NULL,
    created_at date NOT NULL,
    owner_id integer NOT NULL,
    FOREIGN KEY (id) REFERENCES tags (sound_id),
    FOREIGN KEY (owner_id) REFERENCES users (id)
);"""
DATABASE='sounds_database.sqlite3'
db = None
def get_db():
    global db
    if db is None:
        db = sqlite3.connect(DATABASE)
    return db

def close_connection():
    global db
    if db is not None:
        db.close()

def create_table(sql):
    c =get_db()
    try:
        cursor = c.cursor()
        cursor.execute(sql)
    except Exception as e:
        print(e)

def delete_all_rows():
    get_db().cursor().execute('delete from users')

# cursor.execute('insert into users(joined_at,nickname) values(2018-12-5,"pista")')
if __name__ == '__main__':
    cursor = get_db().cursor()
    get_db().commit()
    result =cursor.execute('SELECT COUNT(*) FROM users').fetchall()
    # TO INSERT SOUND:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: sqlite3.Binary(file)
    print(result)
    # create_table(sounds_sql)
    # create_table(users_sql)
    # create_table(tags_sql)
    close_connection()
