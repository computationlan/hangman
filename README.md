# Game of Hangman
This is a Flask implementation of famous children's game Hangman. The user has 6 attempts to guess the hidden word. Each incorrectly guessed letter decreases the number of attempts left. If the user guesses the word with less than 6 incorrect attempts, the user wins. Otherwise, the user loses.

![Screenshot](https://github.com/computationlan/hangman/blob/master/screenshot.png)

# Features
## Difficulty level
The user can choose a difficulty level (provided by the original API with words), the default level is 5 (out of 10).
## Leaderboard
The leaderboard displays the best score for each difficulty level. Once the user wins the game, their score is compared with the current best score and updated if necessary.
## Challenge a friend
Once the user wins the game, they have an option to challenge their friend to guess the same word faster. 
# Instructions
```
brew install python3 sqlite
. setupHangman.sh
FLASK_ENV=development python3 serverHangmanProcess.py
```
