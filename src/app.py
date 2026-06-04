from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'dev'

db = f"dbname='{os.getenv('DB_NAME')}' user='{os.getenv('DB_USER')}' host='{os.getenv('DB_HOST')}' password='{os.getenv('DB_PASSWORD')}'"
conn = psycopg2.connect(db)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/game')
def game():
    if not session.get('started'): # first round, score not initialized
        session['score'] = 0
        session['seen_fens'] = []
        cursor.execute("SELECT fen, num_games FROM positions ORDER BY RANDOM() LIMIT 1")
        session['fen_left'], session['num_games_left'] = cursor.fetchone() # type:ignore
        session['seen_fens'].append(session['fen_left'])
        session.modified = True
        session['started'] = True
    else: # the old _right values become the information for the next guess
        session['fen_left'], session['num_games_left'] = session['fen_right'], session['num_games_right'] 

    cursor.execute("SELECT fen, num_games FROM positions WHERE fen != ALL(%s) ORDER BY RANDOM() LIMIT 1", (session['seen_fens'],))
    session['fen_right'], session['num_games_right'] = cursor.fetchone() # type:ignore
    session['seen_fens'].append(session['fen_right'])
    session.modified = True

    if session['num_games_right'] > session['num_games_left']:
        session['correct_answer'] = 'higher'
    else:
        session['correct_answer'] = 'lower'

    return render_template('game.html', score=session['score'], fen_left=session['fen_left'], fen_right=session['fen_right'],
                            num_games_left=session['num_games_left'], num_games_right=session['num_games_right'] )

@app.route('/guess', methods=['POST'])
def guess():
    answer = request.form['answer']
    correct_answer = session.get('correct_answer')
    if answer == correct_answer:
        return redirect(url_for('correct'))
    else:
        return redirect(url_for('incorrect'))

@app.route('/correct')
def correct():
    session['score'] += 1
    return redirect(url_for('game'))

@app.route('/incorrect')
def incorrect():
    # save score, add to leaderboard ?
    # or track personal best in the corner or something
    session['started'] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
