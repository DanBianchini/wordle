import random
import os

letters = ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '\n', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '\n ', 'z', 'x', 'c', 'v', 'b', 'n', 'm')

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
            result += '\033[30m' + guess[i] # letter not in answer; color black

    return result + '\033[0m' # reset color at the end

def receive_guess() -> str:
    """
    Traps the user in a loop until they give a valid 5-letter response.
    
    :return: Valid guess from user.
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

        print("Only include letters in the response.")

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
            print('\033[30m' + letter + ' ', end='')

    print('\033[0m') # reset ANSI color, newline for spacing

def play_game(word: str) -> bool:
    """
    Play a single game of wordle.
    
    :param word: The answer to be guessed. 5-letter word.
    :type word: str
    :return: True for win, False for loss.
    :rtype: bool
    """
    print(f"\033[95m--- GAME START ---\033[0m\n")

    guess_history = [] # holds previous guesses with ANSI escape codes for coloring
    correct_letter_history = [] # holds previous correct letters
    wrong_letter_history = [] # holds previous wrong letters
    result = False # result of game; default to loss
    
    # 6 turns
    for turn in range(1, 7):
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

        # add guess to guess_history[]
        guess_history.append(color_guess(guess, word))

        # check if guess is correct
        if guess == word:
            result = True
            break

        # add letters to appropriate letter_history[]
        for letter in guess:
            if letter in word:
                if letter not in correct_letter_history:
                    correct_letter_history.append(letter)
            else:
                if letter not in wrong_letter_history:
                    wrong_letter_history.append(letter)
    
    # print letter history
    print_letter_history(correct_letter_history, wrong_letter_history)
    print() # newline for spacing

    # print guess history
    for prev_guess in guess_history:
        print(prev_guess)

    print(f"\n\033[95m--- GAME END ---\033[0m\n")
    return result

def game_cycle() -> None:
    """
    Traps the user in a loop of playing wordle games until they type 'exit'.
    """
    while True:
        u_input = input("Press Enter to play. 'exit' to quit.\n")

        # check if player is trying to quit
        if u_input == 'exit':
            return
        
        word = pick_word() # pick a random word from the list

        # play game & display win/lose message
        if play_game(word):
            print("\033[92mYou win!\033[0m\n")
        else:
            print(f"\033[91mYou lose! The word was \033[93m{word}\033[91m.\033[0m\n")

if __name__ == "__main__":
    game_cycle()
    