# Copyright 2019-2020 Faculty Science Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
from collections import Counter
from words import all_words


CORRECT = 'G'
PRESENT = 'O'
NOT_PRESENT = '.'


class Solver:
    def __init__(self):
        self._possible_words = all_words.copy()
        self._possible_words.sort()

    def get_best_guess(self):
        """Returns the best next guess word."""
        if len(self._possible_words) == len(all_words):
            # Since this is the first guess, and we already know for the best
            # word for first guess, we return it here to save computation time.
            return 'raise'

        # For each of the word in the dictionary, we find entropy again and
        # pick the best one of them. That is our best next guess.
        entries = []
        possible_words = self.get_possible_words()
        for guess in all_words:
            entropy_gain = self._get_entropy_gain(possible_words, guess)
            entries.append((guess, entropy_gain))
        best_guess = max(entries, key=lambda x: x[1])
        return best_guess[0]

    def process_answer(self, guess, pattern):
        """Processes the result of the guess.
        Args:
            guess: The word that was guessed.
            pattern: The pattern returned by wordle.
        """

        possible_words = []
        for word in self._possible_words:
            # Only words which have the same match pattern are a possible
            # solution.
            if get_pattern(word, guess) == pattern:
                possible_words.append(word)
        self._possible_words = possible_words

    def is_solved(self):
        """Returns True if solution is found, False otherwise."""
        return len(self._possible_words) == 1

    def get_possible_words(self):
        """Returns all the current possible solution words."""
        return self._possible_words

    def _get_entropy_gain(self, possible_words, guess):
        """Returns entropy gain the guessed word generated.

        Args:
          possible_words (list<str>): The set of possible words from which we
              have to find solution.
          guessed_word (str): The guessed word.

        Return:
          float: The entropy gain got by the guessed word.
        """
        # This is actually the crux of the solution. How do we measure goodness
        # of the guess? For each guess, when we get the pattern, we should be
        # able to eliminate maximum words. So a guess that supports maximum
        # elimination is the best guess.
        #
        # Let us see between two words how we can consider one is better than
        # other. Imagine out of 22 possible solution words, our first guess
        # generates three different patterns, say "..G..", "OG..." & "...OO",
        # and the word distribution be 20, 1, 1. And another guess generates
        # four patterns with distribution 5, 5, 6, 6.
        #
        # We use shanon's entropy formula to find the entropy of the system
        # before the guess word is applied, and the entropy after the guess
        # is applied. Subtracting these will give us maximum entropy gain.
        c = Counter()
        for word in possible_words:
            c[get_pattern(word, guess)] += 1

        total = 1.0 * len(possible_words)
        entropy = 0
        for pattern, pattern_count in c.items():
            if pattern_count == 1:
                continue
            pi = 1.0 / pattern_count
            entropy -= pattern_count * (pi * math.log(pi) + (1 - pi) * math.log(1 - pi)) * pattern_count / total

        pc = 1 / total
        current_entropy = -1.0  * (pc * math.log(pc) + (1 - pc) * math.log(1 - pc)) * total
        return current_entropy - entropy


def get_pattern(solution_word, guessed_word):
    """Returns the wordle pattern, given solution and the guess words.
    Args:
      solution_word (str): The solution to the wordle problem.
      guessed_word (str): The guess that was given.

    Returns:
      str: The pattern guessed word makes against the solution word.
    """
    word = [w for w in solution_word]
    pattern = ['.'] * 5
    for i, g in enumerate(guessed_word):
        if word[i] == g:
            pattern[i] = CORRECT
            word[i] = ' '
    for i, g in enumerate(guessed_word):
        if pattern[i] == CORRECT:
            continue
        try:
            loc = word.index(g)
            pattern[i] = PRESENT
            word[loc] = ' '
            continue
        except ValueError:
            pass
    return ''.join(pattern)


def is_pattern_ok(pattern):
    if len(pattern) != 5:
        print("** Invalid Pattern **")
        print("Pattern should have exactly 5 characters. Received %d character.\n" % len(pattern))
        return False
    for ch in pattern:
        if ch not in [CORRECT, PRESENT, NOT_PRESENT]:
            print("** Invalid Pattern **")
            print("Pattern should only have any of the three characters from 'G', 'O' & '.'.")
            print("Received character '%s'.\n" % ch)
            return False
    return True
    

def play_all():
    result = {}
    for word in all_words:
        result[word] = play_automatic(word)
    result = sorted(result.items(),  key=lambda x: x[1])
    print(result[:10])
    print(result[-10:])


def play_manual():
    print("Pattern rule: 'G' for green, 'O' for orange and '.' for no match")
    print("Example: 'GO..O'  means Green, Orange, Blank, Blank, Blank.")
    print("")

    solver = Solver()
    attempts = 0
    while not solver.is_solved():
        guess = solver.get_best_guess()
        attempts += 1
        print('\nSuggest you ask this word:', guess)
        while True:
            pattern = input('Input pattern (e.g. G.O.. ): ')
            pattern = pattern.upper()
            if is_pattern_ok(pattern):
                break
        print('Got pattern:', pattern)
        solver.process_answer(guess, pattern)
        print('Number of possible words remaining:', len(solver.get_possible_words()))
        print('Valid words remaining:', solver.get_possible_words())
    print(solver.get_possible_words())
    print('Attempts:', attempts)
    print('\n\n\n')
    return attempts


def play_automatic(word):
    print('=============== Challenge:', word, '==================')
    solver = Solver()
    attempts = 0
    while not solver.is_solved():
        guess = solver.get_best_guess()
        attempts += 1
        print('Ask this word:', guess)
        pattern = get_pattern(word, guess)
        print('Got pattern:', pattern)
        solver.process_answer(guess, pattern)
        print('Number of possible words remaining:', len(solver.get_possible_words()))
        print('Valid words remaining:', solver.get_possible_words())
    print(solver.get_possible_words())
    print('\n\n\n')
    return attempts

if __name__ == '__main__':
    play_manual()
