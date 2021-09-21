from flask import Flask, render_template, request, redirect, jsonify
from flask import json

import sqlite3
from flask import g
from faker import Faker


app = Flask(__name__)

DATABASE = './database.db'


def create_table():
    conn = sqlite3.connect('./database.db')
    conn.execute('CREATE TABLE students (id integer primary key autoincrement, name TEXT, city TEXT)')
    conn.close()

def fetch_data():
    con = sqlite3.connect("./database.db")
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()
    cur.execute("select * from students")
    
    rows = cur.fetchall(); 
    
    return rows

def generate_new_data():
    fake = Faker()
    con = sqlite3.connect("./database.db")
    try:
        with con:
            cur = con.cursor()
            for a in range(3):
                cur.execute("INSERT INTO students (name,city) VALUES (?,?)",(fake.name(),fake.country()) )
                con.commit()
    except:
        con.rollback()
    finally:
        con.close()

@app.route('/')
def home():
    generate_new_data()
    things =fetch_data()

    return render_template('index.html', things=things)

@app.route('/api/')
def api():
    generate_new_data()
    things =fetch_data()
    response={"data":[]}
    
    for data in things:
        response["data"].append(
            {
                "id":data['id'],
                "name":data['name'],
                "city":data['city'],
            }
        )

    return jsonify(response)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    try:
        create_table()
    except:
        pass
    app.run(host='0.0.0.0', port=8000)