import random

# full list of valid words from file
with open('5-letter-words.txt', 'r') as f:
    WORDS = [line.rstrip('\n') for line in f]
    WORDS.sort()

class WordlePal:
    def __init__(self):
        # initialize class variables
        self.valid_words = WORDS.copy() # will store all words that are currently valid guesses
        self.correct_letters = [] # will store all letters that are in the word
        self.guess = None # will store the current guess
        self.answer = "     " # will store the known correct letters in correct places

    def random_guess(self) -> str:
        # if the answer has been completed, give the answer as the next guess
        if ' ' not in self.answer:
            self.guess = self.answer
        # if the answer has not yet been completed, give a random guess from valid_words[]
        else:
            self.guess = self.valid_words[random.randint(0, len(self.valid_words) - 1)] # update self.guess
            self.valid_words.remove(self.guess) # remove the guess from valid_words[] so that it is not used again
        return self.guess

    def smart_guess(self) -> str:
        self.guess = 'guess'
        return self.guess

    def receive_feedback(self, right_place: tuple[bool], in_word: tuple[bool]):
        # check if tuples received are 5 elements in length
        if (len(right_place) != 5) or (len(in_word) != 5):
            raise IndexError('right_place & wrong_place must be tuples of length 5.')
        
        # update class variables
        for i in range(5):
            letter = self.guess[i]
            if in_word[i]:
                self.correct_letters.append(letter) # add the correct letter to correct_letters[]
                if right_place[i]:
                    self.answer = self.answer[:i] + letter + self.answer[i + 1:] # add the correct letter in the correct place to the answer
                    self.valid_words = list(filter(lambda x: x[i] == letter, self.valid_words)) # remove all words from valid_words[] that do NOT have this letter at this position
                else:
                    self.valid_words = list(filter(lambda x: x[i] != letter, self.valid_words)) # remove all words from valid_words[] that have this letter at this position
            else:
                self.valid_words = list(filter(lambda x: True if letter not in x else False, self.valid_words)) # remove all words from valid_words that contain this letter

if __name__ == "__main__":
    wp = WordlePal()
    print(wp.random_guess())