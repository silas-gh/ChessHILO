from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'dev'

db = f"dbname='{os.getenv('DB_NAME')}' user='{os.getenv('DB_USER')}' host='localhost' password='{os.getenv('DB_PASS')}'"
conn = psycopg2.connect(db)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/game')
def game():
    return render_template('game.html')

def get_game_count(fen, token):
    # make request through lichess API, need personal token
    pass

if __name__ == '__main__':
    app.run(debug=True)