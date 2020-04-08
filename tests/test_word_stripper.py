from sliced_art.word_stripper import WordStripper


def test_display():
    all_words = 'lots of words rail the liar sail lairs of lira rails'.split()
    word_stripper = WordStripper(all_words)

    target_letter = 'r'
    word_stripper[target_letter] = 'rails'
    expected_display = 'sail+R -- rail+S, liar+S, lira+S'

    display = word_stripper.make_display(target_letter)

    assert display == expected_display


def test_unknown_word():
    all_words = 'lots of words rail the liar sail lairs of lira rails'.split()
    word_stripper = WordStripper(all_words)

    target_letter = 'i'
    word_stripper[target_letter] = 'rails'
    expected_display = 'rals?I -- rail+S, liar+S, sail+R, lira+S'

    display = word_stripper.make_display(target_letter)

    assert display == expected_display


def test_word_needed():
    all_words = 'lots of words rail the liar sail lairs of lira rails'.split()
    word_stripper = WordStripper(all_words)

    target_letter = 'i'
    word_stripper[target_letter] = ''
    expected_display = 'I word needed'

    display = word_stripper.make_display(target_letter)

    assert display == expected_display


def test_wrong_letter():
    all_words = 'lots of words rail the liar sail lairs of lira rails'.split()
    word_stripper = WordStripper(all_words)

    target_letter = 'i'
    word_stripper[target_letter] = 'food'
    expected_display = 'I word needed'

    display = word_stripper.make_display(target_letter)

    assert display == expected_display


def test_upper_case_word():
    all_words = 'no glib content big man'.split()
    word_stripper = WordStripper(all_words)

    target_letter = 'l'
    word_stripper[target_letter] = 'GLIB'
    expected_display = 'big+L'

    display = word_stripper.make_display(target_letter)

    assert display == expected_display


def test_upper_case_letter():
    all_words = 'no glib content big man'.split()
    word_stripper = WordStripper(all_words)

    target_letter = 'L'
    word_stripper[target_letter] = 'glib'
    expected_display = 'big+L'

    display = word_stripper.make_display(target_letter)

    assert display == expected_display


def test_line_feeds():
    all_words = '''\
no
glib
content
big
man
'''.splitlines(keepends=True)
    word_stripper = WordStripper(all_words)

    target_letter = 'l'
    word_stripper[target_letter] = 'glib'
    expected_display = 'big+L'

    display = word_stripper.make_display(target_letter)

    assert display == expected_display


def test_letter_clues():
    all_words = 'let me tell a tale of a bland land'.split()
    word_stripper = WordStripper(all_words, min_words=2)

    word_stripper['a'] = 'tale'
    expected_clues = dict(a='A', b='B')

    clues = word_stripper.make_clues()

    assert clues == expected_clues


def test_word_clues():
    all_words = 'let me tell a tale of a bland land'.split()
    word_stripper = WordStripper(all_words, min_words=2)

    word_stripper['a'] = 'tale'
    word_stripper['b'] = 'bland'
    expected_clues = dict(a='TALE', b='BLAND')

    clues = word_stripper.make_clues()

    assert clues == expected_clues


def test_make_clues_upper_case_letters():
    all_words = 'let me tell a tale of a bland land'.split()
    word_stripper = WordStripper(all_words, min_words=2)

    word_stripper['A'] = 'tale'
    word_stripper['B'] = 'bland'
    expected_clues = dict(a='TALE', b='BLAND')

    clues = word_stripper.make_clues()

    assert clues == expected_clues


def test_change_word():
    all_words = 'let me tell a tale of a bland land'.split()
    word_stripper = WordStripper(all_words, min_words=2)

    target_letter = 'a'
    word_stripper[target_letter] = 'late'
    word_stripper[target_letter] = 'tale'
    expected_display = 'let+A'

    display = word_stripper.make_display(target_letter)

    assert display == expected_display


def test():
    all_words = 'let me tell a tale of a bland land'.split()
    word_stripper = WordStripper(all_words, min_words=2)

    target_letter = ''
    word_stripper[target_letter] = 'let'
    expected_display = 'tell-L, tale-A'

    display = word_stripper.make_display(target_letter)

    assert display == expected_display
