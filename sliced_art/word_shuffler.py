import re
import typing
from collections import Counter
from random import shuffle


def highlight_letter(word: str, letter: str):
    return word.replace(letter, letter.upper(), 1)


def clean_word(word: str):
    return re.sub(r'\s', '', word).lower()


class WordShuffler:
    def __init__(self,
                 all_words: typing.Optional[typing.Iterable[str]] = None,
                 min_words: int = 0):
        self.min_words = min_words
        if all_words is None:
            cleaned_words = []
        else:
            cleaned_words = (clean_word(word) for word in all_words)
        self.all_letter_counts = {word: Counter(word)
                                  for word in cleaned_words}
        self.words = {}

    def __setitem__(self, letter: str, word: str):
        self.words[letter.lower()] = clean_word(word)

    def __getitem__(self, letter: str):
        return self.words.get(letter.lower(), '')

    def make_display(self, target_letter: str):
        target_letter = target_letter.lower()
        target_word = self[target_letter]
        if not target_word or target_letter not in target_word:
            return f'{target_letter.upper()} word needed.'
        display_parts = [highlight_letter(target_word, target_letter)]
        try:
            target_letter_counts = Counter(self.all_letter_counts[target_word])
        except KeyError:
            target_letter_counts = Counter(target_word)
            display_parts[0] += ' (unknown word)'
        target_letter_counts[target_letter] -= 1
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
        other_words = matches
        if other_words:
            display_parts.append(', '.join(other_words))
        return ' - '.join(display_parts)

    def make_clue(self, target_letter: str):
        target_letter = target_letter.lower()
        default_clue = target_letter.upper()
        if len(self.words) < self.min_words:
            return default_clue
        for other_letter, word in self.words.items():
            if other_letter not in word:
                return default_clue
        target_word = self[target_letter].upper()
        target_letter = default_clue
        clue_letters = list(target_word.replace(target_letter, '', 1))
        if len(clue_letters) == len(target_word):
            return target_letter
        shuffle(clue_letters)
        return ''.join(clue_letters)

    def make_clues(self):
        return {letter: self.make_clue(letter) for letter in self.words}
