import json
from flask import Flask, request, redirect, session, url_for, escape, render_template
from flask.json import jsonify
import requests
import random
import sqlite3

app = Flask(__name__)

app.secret_key = b'qz~y\9K_CU>&uGYM;xcW'

@app.route('/')
def main_page():
    path = "game_of_hangman.html"
    return render_template(path)

@app.route('/game_init', methods=['GET'])
def game_init():
    print('this is game init')
    if request.method == 'GET':
        username = request.args.get('username')
        difficulty = request.args.get('difficulty')
        if 'challenge_id' in request.args:
            session['challenge_id'] = request.args.get('challenge_id')
            conn = sqlite3.connect('hangman.db')
            cur = conn.cursor()
            cur.execute('SELECT challenge, difficulty, score, username FROM challenge_share WHERE share_id = ?', (session['challenge_id'],))
            row = cur.fetchall()
            session['challenge'] = row[0][0]
            session['difficulty'] = row[0][1]
            session['friend_score'] = row[0][2]
        else:
            print('no challenge_id is in')
            response = requests.get("http://app.linkedin-reach.io/words?difficulty="+difficulty)
            session['challenge'] = random.choice(response.text.split('\n')).upper()
        session['username'] = username
        session['difficulty'] = difficulty
        session['wrong_guesses_left'] = 6
        #response = requests.get("http://app.linkedin-reach.io/words?difficulty="+difficulty)
        #print(response.status_code)
        #print(len(response.text))

        #add some error message if nothing is returned on the request - either connection issue or there are no words
        #keyboard should also respond to real actual keyboard, not just on screen buttons

        #print(random.choice(response.text.split('\n')))
        session['guessed'] = ['*']*len(session['challenge'])
        session['wrong_guesses'] = []
        game_json = {'guessed': session['guessed'], 'wrong_guesses_left': session['wrong_guesses_left'], 'game_over':False}
        print(session)
    return json.dumps(game_json)#'New game has started!'

@app.route('/guess_handler')
def guess_handler():
    if request.method == 'GET':
        letter = request.args.get('letterGuessed')
        print('begin', letter, session)
        game_over = False
        share_id = None
        game_over_message = ''
        if letter not in session['challenge'] and letter not in session['wrong_guesses']:
            session['wrong_guesses_left'] -= 1
            if session['wrong_guesses_left'] == 0:
                game_over = True
                game_over_message = 'Sorry, you lost! Try again!'
            wrong_guesses = session['wrong_guesses']
            wrong_guesses.append(letter)
            session['wrong_guesses'] = wrong_guesses
        else:
            currently_guessed = session['guessed']
            for n, each in enumerate(session['challenge']):
                if letter == each:
                    currently_guessed[n] = letter
            session['guessed'] = currently_guessed
            if ''.join(currently_guessed) == session['challenge']:
                game_over = True
                game_over_message = 'Awesome! You won!'
                conn = sqlite3.connect('hangman.db')
                sql = ' UPDATE leaderboard SET score = ? , username = ? WHERE difficulty = ? and score < ? '
                cur = conn.cursor()
                cur.execute(sql, (100*session['wrong_guesses_left'], session['username'], session['difficulty'], 100*session['wrong_guesses_left']))
                conn.commit()

                conn = sqlite3.connect('hangman.db')
                sql = ' INSERT INTO challenge_share (challenge, difficulty, score, username) VALUES(?,?,?,?) '
                cur = conn.cursor()
                cur.execute(sql, (session['challenge'], session['difficulty'], 100*session['wrong_guesses_left'], session['username']))
                share_id = cur.lastrowid
                conn.commit()
        print(session)
    guess_json = {'guessed': session['guessed'], 'wrong_guesses_left': session['wrong_guesses_left'], 'wrong_guesses': session['wrong_guesses'], 'game_over':game_over, 'game_over_message':game_over_message}
    if game_over:
        guess_json['challenge'] = session['challenge']
    if share_id:
        guess_json['share_id'] = share_id
        guess_json['friend_name'] = session['username']
    return json.dumps(guess_json)#'Your guess was ' + str(letter)

@app.route('/leaderboard')
def get_leaderboard():
    conn = sqlite3.connect('hangman.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT difficulty, score, username FROM leaderboard order by difficulty desc')
 
    rows = cur.fetchall()
    
    return json.dumps([dict(row) for row in rows])

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
