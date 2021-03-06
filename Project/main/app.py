from flask import Flask, render_template, g,request,redirect,url_for
import sqlite3
import os
DATABASE = os.path.join('db','sounds_database.sqlite3')


app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
