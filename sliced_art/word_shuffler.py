import typing
from collections import Counter


class WordShuffler:
    def __init__(self, all_words: typing.Iterable[str]):
        self.all_letter_counts = {word: Counter(word) for word in all_words}

    def find_other_words(self, target_word, target_letter):
        target_letter_counts = Counter(target_word)
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
                matches.append(word)
        return matches
