from io import StringIO

import sliced_art.word_shuffler
from sliced_art.word_shuffler import WordShuffler


def mock_shuffle(items: list):
    items.reverse()


def test_setitem():
    word_shuffler = WordShuffler()

    word1 = 'bag'
    letter = 'a'
    word_shuffler[letter] = word1

    word2 = word_shuffler[letter]

    assert word2 == word1


def test_set_item_mixed_case():
    word_shuffler = WordShuffler()

    word1 = 'bag'
    word_shuffler['a'] = word1

    word2 = word_shuffler['A']

    assert word2 == word1


def test_display():
    all_words = 'lots of words rail the liar from his lair with lira'.split()
    word_shuffler = WordShuffler(all_words)

    target_letter = 'a'
    word_shuffler[target_letter] = 'liar'
    expected_display = 'liAr - raIl, laIr, liRa'

    display = word_shuffler.make_display(target_letter)

    assert display == expected_display


def test_display_empty():
    word_shuffler = WordShuffler()

    target_letter = 'e'
    expected_display = 'E word needed.'

    display = word_shuffler.make_display(target_letter)

    assert display == expected_display


def test_display_single():
    all_words = 'the big bag of words'.split()
    word_shuffler = WordShuffler(all_words)

    target_letter = 'e'
    word_shuffler[target_letter] = 'the'
    expected_display = 'thE'

    display = word_shuffler.make_display(target_letter)

    assert display == expected_display


def test_display_mixed_case():
    all_words = 'THE big bag of words'.split()
    word_shuffler = WordShuffler(all_words)

    word_shuffler['E'] = 'tHe'
    expected_display = 'thE'

    display = word_shuffler.make_display('e')

    assert display == expected_display


def test_find_other_words_new_lines():
    all_words = StringIO('''\
the
gab
bag
of
words
''')
    word_shuffler = WordShuffler(all_words)

    target_letter = 'G'
    word_shuffler[target_letter] = 'Bag'
    expected_display = 'baG - gaB'

    display = word_shuffler.make_display(target_letter)

    assert display == expected_display


def test_display_unknown_words():
    all_words = 'THE gob bag of words'.split()
    word_shuffler = WordShuffler(all_words)

    target_letter = 'o'
    word_shuffler[target_letter] = 'bog'
    expected_display = 'bOg (unknown word) - gOb'

    display = word_shuffler.make_display(target_letter)

    assert display == expected_display


def test_display_repeated_letter():
    all_words = 'respect the sceptre of a spectre'.split()
    word_shuffler = WordShuffler(all_words)

    target_letter = 'e'
    word_shuffler[target_letter] = 'respect'
    expected_display = 'rEspect - sCeptre, sPectre'

    display = word_shuffler.make_display(target_letter)

    assert display == expected_display


def test_display_repeated_letter_chosen():
    all_words = 'respect the sceptre of a spectre'.split()
    word_shuffler = WordShuffler(all_words)

    target_letter = 'e'
    word_shuffler[target_letter] = 'respEct'
    expected_display = 'respEct - scepTre, specTre'

    display = word_shuffler.make_display(target_letter)

    assert display == expected_display


def test_display_with_space():
    all_words = 'towards a roasted dinner'.split()
    word_shuffler = WordShuffler(all_words)

    target_letter = 'w'
    word_shuffler[target_letter] = 'to wards'
    expected_display = 'toWards'

    display = word_shuffler.make_display(target_letter)

    assert display == expected_display


def test_display_missing_letter():
    all_words = 'towards a roasted dinner'.split()
    word_shuffler = WordShuffler(all_words)

    target_letter = 'w'
    word_shuffler[target_letter] = 'roasted'
    expected_display = 'W word needed.'

    display = word_shuffler.make_display(target_letter)

    assert display == expected_display


def test_make_clue(monkeypatch):
    monkeypatch.setattr(sliced_art.word_shuffler, 'shuffle', mock_shuffle)
    word_shuffler = WordShuffler()
    target_letter = 'w'
    word_shuffler[target_letter] = 'towards'

    expected_clue = '_ _[_]_ _ _ _\nSDRAWOT'

    clue = word_shuffler.make_clue(target_letter)

    assert clue == expected_clue


def test_make_clue_never_matches():
    word_shuffler = WordShuffler()
    target_letter = 'o'
    word_shuffler[target_letter] = 'mom'

    forbidden_clue = '_[_]_\nMOM'

    for _ in range(100):
        clue = word_shuffler.make_clue(target_letter)

        assert clue != forbidden_clue


def test_make_clue_must_match():
    word_shuffler = WordShuffler()
    target_letter = 'a'
    word_shuffler[target_letter] = 'aa'

    only_clue = '[_]_\nAA'

    clue = word_shuffler.make_clue(target_letter)

    assert clue == only_clue


def test_make_clue_missing_letter():
    word_shuffler = WordShuffler()
    target_letter = 'w'
    word_shuffler[target_letter] = 'rapid'
    expected_clue = 'W'

    clue = word_shuffler.make_clue(target_letter)

    assert clue == expected_clue


def test_make_clue_missing_other_letter():
    word_shuffler = WordShuffler()
    target_letter = 'b'
    word_shuffler[target_letter] = 'blue'
    word_shuffler['w'] = 'rapid'
    expected_clue = 'B'

    clue = word_shuffler.make_clue(target_letter)

    assert clue == expected_clue


def test_make_clue_missing_word():
    word_shuffler = WordShuffler(min_words=2)
    target_letter = 'b'
    word_shuffler[target_letter] = 'blue'
    expected_clue = 'B'

    clue = word_shuffler.make_clue(target_letter)

    assert clue == expected_clue


def test_make_clues(monkeypatch):
    monkeypatch.setattr(sliced_art.word_shuffler, 'shuffle', mock_shuffle)
    word_shuffler = WordShuffler([])
    word_shuffler['a'] = 'black'
    word_shuffler['o'] = 'book'

    expected_clues = dict(a='_ _[_]_ _\nKCALB', o='_[_]_ _\nKOOB')

    clues = word_shuffler.make_clues()

    assert clues == expected_clues
