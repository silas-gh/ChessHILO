from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'dev'

db = f"dbname='chesshilo' user='postgres' host='localhost' password='123'"
db = f"dbname='{os.getenv('DB_NAME')}' user='{os.getenv('DB_USER')}' host='db' password='{os.getenv('DB_PASSWORD')}'"
conn = psycopg2.connect(db)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/game')
def game():
    cursor.execute("SELECT fen, num_games FROM positions ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    fen, num_games = row
    short_fen = fen.split(" ")[0]
    return render_template('game.html', fen=short_fen, num_games=num_games)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
