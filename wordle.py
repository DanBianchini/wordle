import random
import os
import argparse
import matplotlib.pyplot as plt
import text_color as tc
from wordle_pal import WordlePal

DEFAULT_NUM_GAMES = 100 # default # of games to be played by WordlePal when not specified
letters = ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '\n', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '\n ', 'z', 'x', 'c', 'v', 'b', 'n', 'm')
display = True # whether to display game end results when using WordlePal
turns_taken = [0, 0, 0, 0, 0, 0, 0] # will store the # of times each game has ended in each # of turns. turns_taken[0] will represent losses

with open('5-letter-words.txt', 'r') as f:
    WORDS = [line.rstrip('\n') for line in f]

def pick_word() -> str:
    """
    Returns a random word from the list of valid words.
    
    :return: Random word from WORDS[]
    :rtype: str
    """
    return WORDS[random.randint(0, len(WORDS) - 1)]

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
        if guess not in WORDS:
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

def play_game(word: str, wp: WordlePal = None) -> bool:
    """
    Play a single game of wordle.
    
    :param word: The answer to be guessed. 5-letter word.
    :type word: str
    :param wp: WordlePal, if playing.
    :type wp: WordlePal
    :return: True for win, False for loss.
    :rtype: bool
    """
    global turns_taken

    if display:
        print(f"\033[95m--- GAME START ---\033[0m\n")

    guess_history = [] # holds previous guesses with ANSI escape codes for coloring
    correct_letter_history = [] # holds previous correct letters
    wrong_letter_history = [] # holds previous wrong letters
    result = False # result of game; default to loss
    
    # 6 turns
    for turn in range(1, 7):
        # if human is playing, print info and accept guess from user
        if wp is None:
            # print turn number
            print(f"\033[95m--- GUESS #{turn} ---\033[0m")

            # print letter history
            print_letter_history(correct_letter_history, wrong_letter_history)
            print() # newline for spacing

            # print guess history
            for prev_guess in guess_history:
                print(prev_guess)
            print() # newline for spacing

            guess = receive_guess() # receive player guess
            print() # newline for spacing

        # if WordlePal is playing, get guess from it
        else:
            guess = wp.random_guess() # receive WordlePal guess

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

        # TODO: if WordlePal is playing, give feedback
        if wp is not None:
            # create empty lists to store info
            in_word = [] # True if letter is in the answer
            right_place = [] # True if letter is in correct place

            # iterate through guess & answer and compare
            for i in range(5):
                # add to right_place[]
                if guess[i] == word[i]:
                    right_place.append(True)
                else:
                    right_place.append(False)
                
                # add to in_word[]
                if guess[i] in word:
                    in_word.append(True)
                else:
                    in_word.append(False)

            # call class function to give feedback
            wp.receive_feedback(tuple(right_place), tuple(in_word))
    
    # display game-end information if 'display' global variable is set
    if display:
        # print letter history
        print_letter_history(correct_letter_history, wrong_letter_history)
        print() # newline for spacing

        # print guess history
        for prev_guess in guess_history:
            print(prev_guess)

        print(f"\n\033[95m--- GAME END ---\033[0m\n")

    # add # of turns taken to turns_taken[]
    if result:
        turns_taken[turn] += 1
    else:
        turns_taken[0] += 1

    return result

def game_cycle(num_games: int = None, wordle_pal_playing: bool = False) -> None:
    """
    IF NO PARAMETER IS PROVIDED: Traps the user in a loop of playing wordle games until they type 'exit'.
    IF PARAMETER IS PROVIDED: Plays this # of games.

    :param num_games: Number of games for WordlePal to play.
    :type num_games: int
    :param wordle_pal_playing: True if WordlePal is playing.
    :type wordle_pal_playing: bool
    """
    # keep track of game stats during this session
    games_played = 0
    games_won = 0

    while True:
        # if WordlePal is playing, create an instance of WordlePal
        if wordle_pal_playing:
            wp = WordlePal()
        # if user is playing, display game start message
        else:
            wp = None
            u_input = input("Press Enter to play. 'exit' to quit.\n")

            # check if player is trying to quit
            if u_input == 'exit':
                break
        
        word = pick_word() # pick a random word from the list

        # play game & display win/lose message
        if play_game(word, wp):
            games_won += 1 # increment games_won
            # display game win message
            if display:
                print(tc.green("You win!"), end='\n\n')
        else:
            # display game loss message
            if display:
                print(f"{tc.red("You lose!")} The word was {tc.yellow(word)}.", end='\n\n')
        
        games_played += 1 # increment game count

        # if num_games was provided, exit game cycle if num_games has been reached
        if num_games is not None:
            if games_played >= num_games:
                break

def display_stats(graph: bool = False) -> None:
    print('GAME SESSION STATISTICS:')

    # print game session stats
    print(f"{tc.yellow("Games Played:")}\t{sum(turns_taken)}")
    print(f"{tc.green("Games Won:")}\t{sum(turns_taken[1:])}")
    print(f"{tc.red("Games Lost:")}\t{turns_taken[0]}")
    print(f"{tc.blue("Game Win %:")}\t{sum(turns_taken[1:]) * 100 / sum(turns_taken)}%")
    print()

    # display bar graph if requested
    if graph:
        plt.bar(['Loss', '1', '2', '3', '4', '5', '6'], turns_taken)
        plt.title('Games Won in x Turns')
        plt.xlabel('# of Turns Taken')
        plt.ylabel('# of Games')
        plt.show()

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Run to play Wordle. Use the -p option to see WordlePal play.")
    parser.add_argument('-p', '--pal', action='store_true', help="Use this option to have WordlePal play.")
    parser.add_argument('-d', '--display', action='store_true', help="Use this option to display game results when WordlePal is playing.")
    parser.add_argument('-g', '--games', action='store', default=None, type=int, help=f"Use this option to specify the # of games to be played. If not specified when using WordlePal, defaults to {DEFAULT_NUM_GAMES}")
    args = parser.parse_args()

    # check if WordlePal is taking this one
    if args.pal:
        print(tc.rainbow('\nWordlePal will take it from here!\n'))
        if not args.display:
            display = False
        if not args.games:
            raise Exception("Must specify # of games (using -g/--game [GAMES] option) to be played when using WordlePal.")
    
    # start the game cycle
    game_cycle(args.games, args.pal)

    # display stats from game cycle
    display_stats(args.pal)