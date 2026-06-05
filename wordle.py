import random
import os
import argparse
import text_color as tc
from wordle_pal import wordle_pal_guess

letters = ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '\n', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '\n ', 'z', 'x', 'c', 'v', 'b', 'n', 'm')
wordle_pal_playing = False
display = True

with open('5-letter-words.txt', 'r') as f:
    words = [line.rstrip('\n') for line in f]

def pick_word() -> str:
    """
    Returns a random word from the list of valid words.
    
    :return: Random word from words[]
    :rtype: str
    """
    return words[random.randint(0, len(words) - 1)]

def color_guess(guess: str, answer: str) -> str:
    """
    Color 'guess' according to how the letters match with 'answer'.
    Yellow = right letter, wrong place.
    Green = right letter, right place.
    
    :param guess: The player's guess. 5-letter word.
    :type guess: str
    :param answer: The correct answer. 5-letter word.
    :type answer: str
    :return: 'guess' with ANSI escape codes for appropriate coloring.
    :rtype: str
    """
    result = '' # start with empty string

    for i in range(0, 5):
        if guess[i] == answer[i]:
            result += '\033[92m' + guess[i] # right letter, right place; color green
        elif guess[i] in answer:
            result += '\033[93m' + guess[i] # right letter, wrong place; color yellow
        else:
            result += '\033[0m' + guess[i] # letter not in answer; reset color

    return result + '\033[0m' # reset color at the end

def receive_guess() -> str:
    """
    Traps the user in a loop until they give a valid 5-letter response.
    
    :return: Valid guess.
    :rtype: str
    """
    while True:
        guess = input("Enter a guess: ") # accept guess
        guess = guess.lower() # convert to lowercase
        
        # check if word is 5 characters in length
        if len(guess) != 5:
            print("Guess must be 5 letters long.")
            continue

        # check if guess is a valid word
        if guess not in words:
            print("Guess must be a valid 5-letter word")
            continue

        # check if there are only alphabetical letters (no numbers, etc.)
        if guess.isalpha():
            return guess

        print("Guess should only include letters.")

def print_letter_history(correct: list[str], wrong: list[str]):
    """
    Prints the letter history with letters colored if they were correct or wrong.
    
    :param correct: List of correct letters
    :type correct: list[str]
    :param wrong: List of wrong letters
    :type wrong: list[str]
    """
    for letter in letters:
        if letter in correct:
            print('\033[92m' + letter + ' ', end='')
        elif letter in wrong:
            print('\033[91m' + letter + ' ', end='')
        else:
            print('\033[0m' + letter + ' ', end='')

    print('\033[0m') # reset ANSI color, newline for spacing

def play_game(word: str) -> bool:
    """
    Play a single game of wordle.
    
    :param word: The answer to be guessed. 5-letter word.
    :type word: str
    :return: True for win, False for loss.
    :rtype: bool
    """
    if display:
        print(f"\033[95m--- GAME START ---\033[0m\n")

    guess_history = [] # holds previous guesses with ANSI escape codes for coloring
    correct_letter_history = [] # holds previous correct letters
    wrong_letter_history = [] # holds previous wrong letters
    result = False # result of game; default to loss
    
    # 6 turns
    for turn in range(1, 7):
        if display:
            # print turn number
            print(f"\033[95m--- GUESS #{turn} ---\033[0m")

            # print letter history
            print_letter_history(correct_letter_history, wrong_letter_history)
            print() # newline for spacing

            # print guess history
            for prev_guess in guess_history:
                print(prev_guess)
            print() # newline for spacing

        # check if WordlePal is playing
        if wordle_pal_playing:
            guess = wordle_pal_guess()
        else:
            guess = receive_guess() # receive player guess
            print() # newline for spacing

        # add guess to guess_history[]
        guess_history.append(color_guess(guess, word))

        # check if guess is correct
        if guess == word:
            result = True
            if display:
                print(f"\033[95m--- VICTORY IN {turn} TURNS ---\033[0m")
            break

        # add letters to appropriate letter_history[]
        for letter in guess:
            if letter in word:
                if letter not in correct_letter_history:
                    correct_letter_history.append(letter)
            else:
                if letter not in wrong_letter_history:
                    wrong_letter_history.append(letter)
    
    if display:
        # print letter history
        print_letter_history(correct_letter_history, wrong_letter_history)
        print() # newline for spacing

        # print guess history
        for prev_guess in guess_history:
            print(prev_guess)

        print(f"\n\033[95m--- GAME END ---\033[0m\n")

    return result

def game_cycle(num_games: int = None) -> None:
    """
    IF NO PARAMETER IS PROVIDED: Traps the user in a loop of playing wordle games until they type 'exit'.
    IF PARAMETER IS PROVIDED: Plays this # of games.

    :param num_games: Number of games for WordlePal to play.
    :type num_games: int
    """
    # keep track of game stats during this session
    games_played = 0
    games_won = 0
    games_lost = 0

    while True:
        # if user is playing, display game start message
        if not wordle_pal_playing:
            u_input = input("Press Enter to play. 'exit' to quit.\n")

            # check if player is trying to quit
            if u_input == 'exit':
                break
        
        word = pick_word() # pick a random word from the list

        # play game & display win/lose message
        if play_game(word):
            games_won += 1 # increment games_won
            # display game win message
            if display:
                print(tc.green("You win!"), end='\n\n')
        else:
            games_lost += 1 # increment games_lost
            # display game loss message
            if display:
                print(f"{tc.red("You lose!")} The word was {tc.yellow(word)}.", end='\n\n')
        
        games_played += 1 # increment game count

        # if num_games was provided, exit game cycle if num_games has been reached
        if num_games is not None:
            if games_played >= num_games:
                break

    # print game session stats
    print(f"{tc.yellow("Games Played:")} {games_played}")
    print(f"{tc.green("Games Won:")} {games_won}")
    print(f"{tc.red("Games Lost:")} {games_lost}")
    print()

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Run to play Wordle. Use the -p option to see WordlePal play.")
    parser.add_argument('-p', '--pal', action='store_true', help="Use this option to have WordlePal play.")
    args = parser.parse_args()

    # check if WordlePal is taking this one
    if args.pal:
        print('\nWordlePal will take it from here!')
        wordle_pal_playing = True
        display = False
        game_cycle(100)
    else:
        game_cycle()
