import re
import typing
from collections import defaultdict
from random import shuffle


def highlight_position(word: str, position: int):
    return word[:position] + word[position].upper() + word[position+1:]


def anagram_root(word: str):
    return ''.join(sorted(word))


def clean_word(word: str, force_lower: bool = True):
    stripped = re.sub(r'\s', '', word)
    if force_lower:
        stripped = stripped.lower()
    return stripped


class WordShuffler:
    def __init__(self,
                 all_words: typing.Optional[typing.Iterable[str]] = None,
                 min_words: int = 0):
        self.min_words = min_words
        self.anagrams = defaultdict(list)
        if all_words is not None:
            for word in all_words:
                cleaned_word = clean_word(word)
                root = anagram_root(cleaned_word)
                root_anagrams = self.anagrams[root]
                root_anagrams.append(cleaned_word)
        self.words = {}
        self.targets = {}

    def __setitem__(self, letter: str, word: str):
        letter = letter.lower()
        word = clean_word(word, False)
        upper_target_letter = letter.upper()
        target_pos = word.find(upper_target_letter)
        if target_pos < 0:
            target_pos = word.find(letter)
        self.words[letter] = word.lower()
        self.targets[letter] = target_pos

    def __getitem__(self, letter: str):
        return self.words.get(letter.lower(), '')

    def make_display(self, target_letter: str):
        target_letter = target_letter.lower()
        target_word = self[target_letter]
        upper_target_letter = target_letter.upper()
        target_pos = self.targets.get(target_letter, -1)
        if not target_word or target_pos < 0:
            return f'{upper_target_letter} word needed.'

        display_parts = [highlight_position(target_word, target_pos)]
        word_anagrams = self.anagrams[anagram_root(target_word)]
        matches = []
        is_known = False
        for word_anagram in word_anagrams:
            if word_anagram == target_word:
                is_known = True
                continue
            matches.append(highlight_position(word_anagram, target_pos))
        if not is_known:
            display_parts[0] += ' (unknown word)'
        other_words = matches
        if other_words:
            display_parts.append(', '.join(other_words))
        return ' - '.join(display_parts)

    def make_clue(self, target_letter: str):
        target_letter = target_letter.lower()
        default_clue = target_letter.upper()
        if len(self.words) < self.min_words:
            return default_clue
        if any(pos < 0 for pos in self.targets.values()):
            return default_clue
        target_word = self[target_letter].upper()
        clue_letters = list(target_word)
        letter_text = None
        for _ in range(10):
            shuffle(clue_letters)
            letter_text = ''.join(clue_letters)
            if letter_text != target_word:
                break
        target_pos = self.targets[target_letter]
        blanks = [' ', '_'] * len(target_word) + [' ']
        blanks[target_pos*2:target_pos*2+1] = '['
        blanks[target_pos*2+2:target_pos*2+3] = ']'
        blank_text = ''.join(blanks).strip()
        return blank_text + '\n' + letter_text

    def make_clues(self):
        return {letter: self.make_clue(letter) for letter in self.words}
