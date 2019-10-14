#!/bin/bash
rm -rf venv
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt

sqlite3 hangman.db "drop table if exists leaderboard;"
sqlite3 hangman.db "drop table if exists challenge_share;"
sqlite3 hangman.db "create table leaderboard (difficulty integer primary key, score integer not null, username text not null);"
sqlite3 hangman.db "insert into leaderboard (difficulty, score, username) values (1, 0, 'Anonymous');"
sqlite3 hangman.db "insert into leaderboard (difficulty, score, username) values (2, 0, 'Anonymous');"
sqlite3 hangman.db "insert into leaderboard (difficulty, score, username) values (3, 0, 'Anonymous');"
sqlite3 hangman.db "insert into leaderboard (difficulty, score, username) values (4, 0, 'Anonymous');"
sqlite3 hangman.db "insert into leaderboard (difficulty, score, username) values (5, 0, 'Anonymous');"
sqlite3 hangman.db "insert into leaderboard (difficulty, score, username) values (6, 0, 'Anonymous');"
sqlite3 hangman.db "insert into leaderboard (difficulty, score, username) values (7, 0, 'Anonymous');"
sqlite3 hangman.db "insert into leaderboard (difficulty, score, username) values (8, 0, 'Anonymous');"
sqlite3 hangman.db "insert into leaderboard (difficulty, score, username) values (9, 0, 'Anonymous');"
sqlite3 hangman.db "insert into leaderboard (difficulty, score, username) values (10, 0, 'Anonymous');"
sqlite3 hangman.db "create table challenge_share (share_id integer primary key, challenge text not null, difficulty integer, score integer not null, username text not null);"

