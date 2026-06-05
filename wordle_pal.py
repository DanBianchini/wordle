import random

with open('5-letter-words.txt', 'r') as f:
    words = [line.rstrip('\n') for line in f]

def wordle_pal_guess() -> str:
    return words[random.randint(0, len(words) - 1)]

if __name__ == "__main__":
    print(wordle_pal_guess())