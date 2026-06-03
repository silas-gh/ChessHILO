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
    return render_template('game.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)