from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import re
import bcrypt
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

username_regex = r'^[a-zA-Z0-9_-]{3,30}$'
password_regex = r'.{3,30}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT user_id, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            session['user_id'] = str(user[0])
            session['username'] = username
            session['is_guest'] = False
            session['started'] = False
            return redirect('/dashboard')
        else:
            return render_template('login.html', error_msg="Incorrect username or password")
    
    return render_template('login.html', error_msg=None)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if not re.match(username_regex, username):
            return render_template('register.html', error_msg="Invalid username")
        if not re.match(password_regex, password):
            return render_template('register.html', error_msg="Invalid password")
        if password != confirm_password:
            return render_template('register.html', error_msg="Password does not match with confirm password")
        cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        name_already_used = cursor.fetchone()
        if name_already_used:
            return render_template('register.html', error_msg="Username already used")
        
        password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        return redirect('/login')

    return render_template('register.html', error_msg=None)




@app.route('/guest')
def guest():
    session.pop('user_id', None)
    session['username'] = None
    session['is_guest'] = True
    session['started'] = False
    return redirect('/dashboard')

def user_has_auth():
    return session.get('username') or session.get('is_guest')

@app.route('/dashboard')
def dashboard():
    if not user_has_auth():
        return redirect('/login')
    session['started'] = False
    return render_template('dashboard.html')

@app.route('/signout')
def signout():
    session.clear()
    return redirect('/')

@app.route('/game')
def game():
    if not user_has_auth():
        return redirect('/login')
    if not session.get('started'): # first round, score not initialized
        session['started'] = True
        session['score'] = 0
        session['seen_fens'] = []
        cursor.execute("SELECT fen, num_games FROM positions ORDER BY RANDOM() LIMIT 1")
        session['fen_left'], session['num_games_left'] = cursor.fetchone() # type:ignore
        session['seen_fens'].append(session['fen_left'])
        session.modified = True
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
        return redirect('/correct')
    else:
        return redirect('/incorrect')

@app.route('/correct')
def correct():
    session['score'] += 1
    return redirect('/game')

@app.route('/incorrect')
def incorrect():
    user_id = session.get('user_id')
    score = session.get('score', 0)

    print("saving score:", score, "for user_id:", user_id)

    if user_id:
        cursor.execute("""
            INSERT INTO leaderboard (user_id, score)
            VALUES (%s, %s)
            ON CONFLICT (user_id)
            DO UPDATE SET score = GREATEST(leaderboard.score, EXCLUDED.score)
        """, (user_id, session.get('score', 0)))
        conn.commit()

    session['started'] = False
    return redirect('/leaderboard')

@app.route('/leaderboard')
def leaderboard():
    cursor.execute("""
        SELECT users.username, leaderboard.score
        FROM leaderboard
        JOIN users ON leaderboard.user_id = users.user_id
        ORDER BY leaderboard.score DESC, users.username ASC
        LIMIT 10
    """)

    scores = cursor.fetchall()

    return render_template('leaderboard.html', scores=scores)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
