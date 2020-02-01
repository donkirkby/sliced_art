from io import StringIO

import pytest

import sliced_art.word_shuffler
from sliced_art.word_shuffler import WordShuffler


def mock_shuffle(items: list):
    items.reverse()


def test_find_other_words():
    all_words = 'the big bag of words'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = 'bag'
    target_letter = 'a'
    expected_words = ['bIg']

    other_words = word_shuffler.find_other_words(target_word, target_letter)

    assert other_words == expected_words


def test_find_other_words_mixed_case():
    all_words = 'the BIG bag of words'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = 'Bag'
    target_letter = 'A'
    expected_words = ['bIg']

    other_words = word_shuffler.find_other_words(target_word, target_letter)

    assert other_words == expected_words


def test_find_other_words_new_lines():
    all_words = StringIO('''\
the
BIG
bag
of
words
''')
    word_shuffler = WordShuffler(all_words)

    target_word = 'Bag'
    target_letter = 'A'
    expected_words = ['bIg']

    other_words = word_shuffler.find_other_words(target_word, target_letter)

    assert other_words == expected_words


def test_display():
    all_words = 'the big bag of gob words'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = 'bag'
    target_letter = 'a'
    expected_display = 'bAg - bIg, gOb'

    display = word_shuffler.display(target_word, target_letter)

    assert display == expected_display


def test_display_empty():
    all_words = 'the big bag of words'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = ''
    target_letter = 'e'
    expected_display = 'E word needed.'

    display = word_shuffler.display(target_word, target_letter)

    assert display == expected_display


def test_display_single():
    all_words = 'the big bag of words'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = 'the'
    target_letter = 'e'
    expected_display = 'thE'

    display = word_shuffler.display(target_word, target_letter)

    assert display == expected_display


def test_display_mixed_case():
    all_words = 'THE big bag of words'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = 'tHe'
    target_letter = 'E'
    expected_display = 'thE'

    display = word_shuffler.display(target_word, target_letter)

    assert display == expected_display


def test_display_unknown_words():
    all_words = 'THE big bag of words'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = 'unflerging'
    target_letter = 'e'
    expected_display = 'Unknown word!'

    display = word_shuffler.display(target_word, target_letter)

    assert display == expected_display


def test_display_repeated_letter():
    all_words = 'the big book of words'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = 'book'
    target_letter = 'o'
    expected_display = 'bOok'

    display = word_shuffler.display(target_word, target_letter)

    assert display == expected_display


def test_display_with_space():
    all_words = 'towards a roasted dinner'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = 'to wards'
    target_letter = 'w'
    expected_display = 'toWards - roastEd'

    display = word_shuffler.display(target_word, target_letter)

    assert display == expected_display


def test_display_missing_letter():
    all_words = 'towards a roasted dinner'.split()
    word_shuffler = WordShuffler(all_words)

    target_word = 'roasted'
    target_letter = 'w'
    expected_display = 'W word needed.'

    display = word_shuffler.display(target_word, target_letter)

    assert display == expected_display


def test_make_clue(monkeypatch):
    monkeypatch.setattr(sliced_art.word_shuffler, 'shuffle', mock_shuffle)
    word_shuffler = WordShuffler([])
    target_word = 'towards'
    target_letter = 'w'

    expected_clue = 'SDRAOT'

    clue = word_shuffler.make_clue(target_word, target_letter)

    assert clue == expected_clue


def test_make_clue_missing_letter():
    word_shuffler = WordShuffler([])
    target_word = 'rapid'
    target_letter = 'w'

    with pytest.raises(ValueError) as ctx:
        word_shuffler.make_clue(target_word, target_letter)

    assert ctx.value.args == ('No W in RAPID.',)


def test(monkeypatch):
    monkeypatch.setattr(sliced_art.word_shuffler, 'shuffle', mock_shuffle)
    word_shuffler = WordShuffler([])
    target_word = 'book'
    target_letter = 'o'

    expected_clue = 'KOB'

    clue = word_shuffler.make_clue(target_word, target_letter)

    assert clue == expected_clue
