import typing
from collections import defaultdict, Counter


class WordStripper:
    def __init__(self, all_words=None, min_words=0):
        self.needs_blank = True
        self.all_words = list(all_words)
        self.all_words_by_size = defaultdict(list)
        for word in self.all_words:
            word = word.strip()
            size_list = self.all_words_by_size[len(word)]
            size_list.append(word)
        start = ord('a')
        self.words = {chr(i): ''
                      for i in range(start, start+min_words)}  # {letter: word}
        self.words[''] = ''
        self.goal_words = defaultdict(list)  # {letter: [(word, letter)]}
        self.other_words = defaultdict(list)  # {letter: [(word, letter)]}

    def __setitem__(self, letter: str, word: str):
        letter = letter.lower()
        self.words[letter] = word
        word = word.lower()
        self.goal_words[letter] = goal_word_list = []
        self.other_words[letter] = other_word_list = []
        if letter:
            source_words = self.all_words_by_size[len(word) - 1]
        else:
            source_words = self.all_words_by_size[len(word) + 1]
        target_counts = Counter(word)
        for source_word in source_words:
            source_counts = Counter(source_word)

            # diffs doesn't include negative or zero values!
            if letter:
                diffs = target_counts - source_counts
            else:
                diffs = source_counts - target_counts
            if sum(diffs.values()) == 1:
                extra_letter, = diffs
                if extra_letter == letter:
                    goal_word_list.append((source_word, extra_letter))
                else:
                    other_word_list.append((source_word, extra_letter))

    def __getitem__(self, letter: str) -> str:
        return self.words[letter.lower()]

    def make_display(self, letter: str) -> str:
        letter = letter.lower()
        word = self.words[letter].lower()
        if not letter:
            return self.make_subtraction_display(letter)
        if letter not in word:
            return f'{letter.upper()} word needed'
        display = display_word_list(self.goal_words[letter])
        if not display:
            i = word.index(letter)
            display = f'{word[:i]}{word[i+1:]}?{letter.upper()}'
        other_words_display = display_word_list(self.other_words[letter])
        if other_words_display:
            display = f'{display} -- {other_words_display}'
        return display

    def make_subtraction_display(self, letter: str):
        return ', '.join(f'{word}-{extra_letter.upper()}'
                         for word, extra_letter in self.other_words[letter])

    def make_clues(self) -> typing.Dict[str, str]:
        if any(letter not in word.lower()
               for letter, word in self.words.items()):
            return {letter: letter.upper() for letter in self.words if letter}
        return {letter: word.upper()
                for letter, word in self.words.items()
                if letter}


def display_word_list(word_list: typing.List[typing.Tuple[str, str]]) -> str:
    return ', '.join(f'{word}+{letter.upper()}' for word, letter in word_list)
