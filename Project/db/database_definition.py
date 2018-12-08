from flask import Flask, render_template, g,request,redirect,url_for
import sqlite3
import os

tags_sql="""CREATE TABLE IF NOT EXISTS tags(
    sound_id integer NOT NULL,
    name text NOT NULL
);"""

users_sql="""CREATE TABLE IF NOT EXISTS users(
    id integer PRIMARY KEY,
    joined_at DATE NOT NULL DEFAULT (datetime('now')),
    nickname text NOT NULL
);"""


sounds_sql=""" CREATE TABLE IF NOT EXISTS sounds(
    id integer PRIMARY KEY,
    name text NOT NULL,
    data blob NOT NULL,
    likes integer NOT NULL DEFAULT 0,
    dislikes integer NOT NULL DEFAULT 0,
    created_at date NOT NULL DEFAULT (datetime('now')),
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

def insert_to_users_from_sample():
    with open(os.path.join("samples",'users_sample.txt')) as f:
        for line in f:
            (id,joined_at,nickname)=list(map(lambda x:x.strip(),line.split(';')))
            get_db().cursor().execute('insert into users values(?,?,?)',(id,joined_at,nickname))
        get_db().commit()

def insert_to_tags_from_sample():
    with open(os.path.join("samples",'tags_sample.txt')) as f:
        for line in f:
            (sound_id,name)=list(map(lambda x:x.strip(),line.split(';')))
            get_db().cursor().execute('insert into tags values(?,?)',(sound_id,name))
        get_db().commit()

def insert_to_sounds_from_sample():
    with open(os.path.join("samples",'sounds_sample.txt')) as f:
        for line in f:
            (id,name,blob_path,_2,_3,_4,owner_id)=list(map(lambda x:x.strip(),line.split(';')))
            with open(os.path.join('sound_samples',blob_path+'.mp3'), 'rb') as fl:
                data = fl.read()
            get_db().cursor().execute('insert into sounds(id,name,data,owner_id) values(?,?,?,?)',(id,name,sqlite3.Binary(data),owner_id))
        get_db().commit()

if __name__ == '__main__':
    cursor = get_db().cursor()
    results = cursor.execute('select * from users').fetchall()
    for result in results:
        print(result)
    close_connection()


# cursor.execute('insert into users(joined_at,nickname) values(2018-12-5,"pista")')

# cursor.execute('drop table users')
# cursor.execute('drop table sounds')
# cursor.execute('drop table tags')

# create_table(sounds_sql)
# create_table(users_sql)
# create_table(tags_sql)
