from sliced_art.word_shuffler import WordShuffler


def test():
    all_words = 'the big bag of words'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = 'bag'
    target_letter = 'a'
    expected_words = ['big']

    other_words = word_shuffler.find_other_words(target_word, target_letter)

    assert other_words == expected_words
