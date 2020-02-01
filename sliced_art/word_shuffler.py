import re
import typing
from collections import Counter
from random import shuffle


def highlight_letter(word: str, letter: str):
    return word.replace(letter, letter.upper(), 1)


def clean_word(word: str):
    return re.sub(r'\s', '', word).lower()


class WordShuffler:
    def __init__(self, all_words: typing.Iterable[str]):
        cleaned_words = (clean_word(word) for word in all_words)
        self.all_letter_counts = {word: Counter(word)
                                  for word in cleaned_words}

    def find_other_words(self, target_word, target_letter):
        target_word = clean_word(target_word)
        target_letter_counts = Counter(self.all_letter_counts[target_word])
        target_letter_counts[target_letter.lower()] -= 1
        matches = []
        for word, letter_counts in self.all_letter_counts.items():
            if word == target_word:
                continue
            counts_diff = Counter(letter_counts)
            counts_diff.subtract(target_letter_counts)
            if any(n < 0 for n in counts_diff.values()):
                continue
            if sum(counts_diff.values()) == 1:
                extra_letter = [c
                                for c, count in counts_diff.items()
                                if count == 1][0]
                matches.append(highlight_letter(word, extra_letter))
        return matches

    def display(self, target_word: str, target_letter: str):
        target_word = clean_word(target_word)
        target_letter = target_letter.lower()
        if not target_word or target_letter not in target_word:
            return f'{target_letter.upper()} word needed.'
        display_parts = [highlight_letter(target_word, target_letter)]
        try:
            other_words = self.find_other_words(target_word, target_letter)
        except KeyError:
            return 'Unknown word!'
        if other_words:
            display_parts.append(', '.join(other_words))
        return ' - '.join(display_parts)

    @staticmethod
    def make_clue(target_word: str, target_letter: str):
        target_word = clean_word(target_word).upper()
        target_letter = target_letter.upper()
        clue_letters = list(target_word.replace(target_letter, '', 1))
        if len(clue_letters) == len(target_word):
            raise ValueError(f'No {target_letter} in {target_word}.')
        shuffle(clue_letters)
        return ''.join(clue_letters)
