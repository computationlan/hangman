from flask import Flask, request, session, render_template
from flask.json import jsonify
import requests
import random
import sqlite3

app = Flask(__name__)

app.secret_key = b"qz~y\9K_CU>&uGYM;xcW"


def get_db():
    conn = sqlite3.connect("hangman.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def main_page():
    path = "game_of_hangman.html"
    return render_template(path)


@app.route("/game_init")
def game_init():
    username = request.args.get("username")
    difficulty = request.args.get("difficulty")
    challenge_id = request.args.get("challenge_id")
    session.clear()
    if challenge_id:
        cur = get_db().cursor()
        cur.execute(
            " SELECT challenge, difficulty, score, username FROM challenge_share WHERE share_id = ? ", (challenge_id,)
        )
        row = cur.fetchone()
        session["challenge_id"] = challenge_id
        session["challenge"] = row["challenge"]
        session["difficulty"] = row["difficulty"]
        session["friend_score"] = row["score"]
        session["friend_name"] = row["username"]
    else:
        response = requests.get("http://app.linkedin-reach.io/words?difficulty=" + difficulty)
        app.logger.debug((response.status_code, len(response.text)))
        if response.status_code != 200 or len(response.text) < 1:
            session["challenge"] = "LINKEDIN"
        else:
            session["challenge"] = random.choice(response.text.split("\n")).upper()
        session["difficulty"] = difficulty
    session["username"] = username
    session["guessed"] = ["*"] * len(session["challenge"])
    session["wrong_guesses_left"] = 6
    session["wrong_guesses"] = []
    app.logger.debug(session)
    game_json = {
        "guessed": session["guessed"],
        "wrong_guesses_left": session["wrong_guesses_left"],
        "wrong_guesses": [],
        "game_over": False,
        "game_over_message": "",
    }
    return jsonify(game_json)


@app.route("/guess_handler")
def guess_handler():
    letter = request.args.get("letterGuessed")
    game_over = False
    share_id = None
    game_over_message = ""
    if letter not in session["challenge"]:
        session["wrong_guesses_left"] -= 1
        wrong_guesses = session["wrong_guesses"]
        wrong_guesses.append(letter)
        session["wrong_guesses"] = wrong_guesses
    else:
        currently_guessed = session["guessed"]
        for n, each in enumerate(session["challenge"]):
            if letter == each:
                currently_guessed[n] = letter
        session["guessed"] = currently_guessed
    if "".join(session["guessed"]) == session["challenge"]:
        score = 100 * session["wrong_guesses_left"]
        conn = get_db()
        cur = conn.cursor()
        sql = " UPDATE leaderboard SET score = ?, username = ? WHERE difficulty = ? and score < ? "
        cur.execute(sql, (score, session["username"], session["difficulty"], score))
        sql = " INSERT INTO challenge_share (challenge, difficulty, score, username) VALUES(?, ?, ?, ?) "
        cur.execute(sql, (session["challenge"], session["difficulty"], score, session["username"]))
        share_id = cur.lastrowid
        conn.commit()
        game_over = True
        game_over_message = "Awesome! You won! Your score is " + str(score) + ". "
        if "friend_name" in session:
            game_over_message += session["friend_name"] + "'s score was " + str(session["friend_score"])
        game_over_message += (
            '<br/><a href="/?share_id='
            + str(share_id)
            + "&friend_name="
            + str(session["username"])
            + '">Want to share this challenge with your friend?</a>'
        )
        if "friend_name" in session:
            game_over_message += '<br/>If you want to play again with a new word, <a href="/">click here</a>.'
    elif session["wrong_guesses_left"] == 0:
        game_over = True
        game_over_message = "Sorry, you lost! Try again!"
        if "friend_name" in session:
            game_over_message += '<br/>If you want to play again with a new word, <a href="/">click here</a>.'
    guess_json = {
        "guessed": session["guessed"],
        "wrong_guesses_left": session["wrong_guesses_left"],
        "wrong_guesses": session["wrong_guesses"],
        "game_over": game_over,
        "game_over_message": game_over_message,
    }
    if game_over:
        guess_json["challenge"] = session["challenge"]
    app.logger.debug(session)
    app.logger.debug(guess_json)
    return jsonify(guess_json)


@app.route("/leaderboard")
def get_leaderboard():
    cur = get_db().cursor()
    sql = " SELECT difficulty, score, username FROM leaderboard ORDER BY difficulty DESC "
    cur.execute(sql)
    rows = cur.fetchall()
    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
