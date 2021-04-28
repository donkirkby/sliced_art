import pytest
from PySide6.QtGui import Qt, QPixmap, QPainter, QColor, QPen, QBrush
from PySide6.QtWidgets import QApplication

from sliced_art.art_shuffler import ArtShuffler
from tests.pixmap_differ import PixmapDiffer


@pytest.fixture(scope='session')
def pixmap_differ():
    app = QApplication()

    yield PixmapDiffer()

    assert app


@pytest.fixture()
def symbol_clues():
    transparent = QColor(255, 255, 255, 0)
    green = QColor('green')
    symbol_pen = QPen(QBrush(green), 30)
    row1 = QPixmap(900, 900)
    row1.fill(transparent)
    painter = QPainter(row1)
    painter.setPen(symbol_pen)
    painter.drawLine(100, 100, 800, 100)
    painter.end()
    row2 = QPixmap(900, 900)
    row2.fill(transparent)
    painter = QPainter(row2)
    painter.setPen(symbol_pen)
    painter.drawLine(100, 700, 800, 700)
    painter.end()
    col1 = QPixmap(900, 900)
    col1.fill(transparent)
    painter = QPainter(col1)
    painter.setPen(symbol_pen)
    painter.drawLine(10, 10, 100, 700)
    painter.end()
    col2 = QPixmap(900, 900)
    col2.fill(transparent)
    painter = QPainter(col2)
    painter.setPen(symbol_pen)
    painter.drawLine(890, 10, 800, 800)
    painter.end()
    return [row1, row2], [col1, col2]


def outline_rect(painter: QPainter,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 colour: QColor,
                 pen_width: int = 2):
    old_pen = painter.pen()
    grey_pen = QPen(QColor('lightgrey'))
    grey_pen.setWidth(pen_width)
    painter.setPen(grey_pen)
    painter.drawRect(x, y, width, height)
    painter.fillRect(x, y, width, height, colour)
    painter.setPen(old_pen)


# noinspection DuplicatedCode
def test_art_shuffler_square(pixmap_differ):
    art = QPixmap(1000, 1000)
    painter = QPainter(art)
    green = QColor('green')
    blue = QColor('blue')
    painter.fillRect(0, 0, 500, 1000, green)
    painter.fillRect(500, 0, 500, 1000, blue)
    painter.end()

    actual, expected = pixmap_differ.start(200, 200, 'art_shuffler_square')
    outline_rect(expected, 5, 0, 90, 90, green, pen_width=3)
    outline_rect(expected, 5, 100, 90, 90, green, pen_width=3)
    outline_rect(expected, 105, 0, 90, 90, blue, pen_width=3)
    outline_rect(expected, 105, 100, 90, 90, blue, pen_width=3)

    actual.end()
    shuffler = ArtShuffler(2, 2, actual.device())
    shuffler.draw(art)

    pixmap_differ.assert_equal()


def test_art_shuffler_not_square(pixmap_differ):
    art = QPixmap(1000, 500)
    painter = QPainter(art)
    green = QColor('green')
    blue = QColor('blue')
    painter.fillRect(0, 0, 500, 500, green)
    painter.fillRect(500, 0, 500, 500, blue)
    painter.end()

    actual, expected = pixmap_differ.start(200,
                                           100,
                                           'test_art_shuffler_not_square')
    outline_rect(expected, 7, 0, 90, 45, green, pen_width=3)
    outline_rect(expected, 7, 50, 90, 45, green, pen_width=3)
    outline_rect(expected, 102, 0, 90, 45, blue, pen_width=3)
    outline_rect(expected, 102, 50, 90, 45, blue, pen_width=3)

    actual.end()
    shuffler = ArtShuffler(2, 2, actual.device())
    shuffler.draw(art)

    pixmap_differ.assert_equal()


# noinspection DuplicatedCode
def test_art_shuffler_aspect(pixmap_differ):
    art = QPixmap(1000, 1000)
    painter = QPainter(art)
    green = QColor('green')
    blue = QColor('blue')
    painter.fillRect(0, 0, 500, 1000, green)
    painter.fillRect(500, 0, 500, 1000, blue)
    painter.end()

    actual, expected = pixmap_differ.start(200, 100, 'test_art_shuffler_aspect')
    outline_rect(expected, 52, 0, 45, 45, green)
    outline_rect(expected, 52, 50, 45, 45, green)
    outline_rect(expected, 102, 0, 45, 45, blue)
    outline_rect(expected, 102, 50, 45, 45, blue)

    actual.end()
    shuffler = ArtShuffler(2, 2, actual.device())
    shuffler.draw(art)

    pixmap_differ.assert_equal()


# noinspection DuplicatedCode
def test_art_shuffler_clears(pixmap_differ):
    art = QPixmap(1000, 1000)
    painter = QPainter(art)
    green = QColor('green')
    blue = QColor('blue')
    painter.fillRect(0, 0, 500, 1000, green)
    painter.fillRect(500, 0, 500, 1000, blue)
    painter.end()

    actual, expected = pixmap_differ.start(200, 200, 'test_art_shuffler_clears')
    outline_rect(expected, 5, 0, 90, 90, green, pen_width=3)
    outline_rect(expected, 5, 100, 90, 90, green, pen_width=3)
    outline_rect(expected, 105, 0, 90, 90, blue, pen_width=3)
    outline_rect(expected, 105, 100, 90, 90, blue, pen_width=3)

    # Pollute the display with a previous version.
    actual.fillRect(50, 50, 100, 100, blue)

    actual.end()
    shuffler = ArtShuffler(2, 2, actual.device())
    shuffler.draw(art)

    pixmap_differ.assert_equal()


# noinspection DuplicatedCode
def test_art_shuffler_shuffle(pixmap_differ, monkeypatch):
    monkeypatch.setattr('sliced_art.art_shuffler.shuffle',
                        lambda a: a.reverse())

    art = QPixmap(900, 900)
    painter = QPainter(art)
    green = QColor('green')
    blue = QColor('blue')
    painter.fillRect(0, 0, 450, 1000, green)
    painter.fillRect(450, 0, 450, 1000, blue)
    painter.fillRect(150, 150, 150, 150, blue)
    painter.end()

    actual, expected = pixmap_differ.start(200, 200, 'test_art_shuffler_shuffle')
    outline_rect(expected, 20, 0, 60, 60, blue)
    outline_rect(expected, 20, 100, 60, 60, blue)
    outline_rect(expected, 120, 0, 60, 60, green)
    outline_rect(expected, 120, 100, 60, 60, green)
    expected.fillRect(140, 120, 20, 20, blue)

    font = expected.font()
    font.setPixelSize(15)
    expected.setFont(font)
    expected.drawText(0, 60, 100, 15, Qt.AlignmentFlag.AlignHCenter, 'D')
    expected.drawText(100, 60, 100, 15, Qt.AlignmentFlag.AlignHCenter, 'C')
    expected.drawText(0, 160, 100, 15, Qt.AlignmentFlag.AlignHCenter, 'B')
    expected.drawText(100, 160, 100, 15, Qt.AlignmentFlag.AlignHCenter, 'A')

    actual.end()
    shuffler = ArtShuffler(2, 2, actual.device())

    shuffler.shuffle()
    shuffler.draw(art)

    pixmap_differ.assert_equal()


# noinspection DuplicatedCode
def test_art_shuffler_shuffle_clues(pixmap_differ, monkeypatch):
    monkeypatch.setattr('sliced_art.art_shuffler.shuffle',
                        lambda a: a.reverse())

    art = QPixmap(900, 900)
    painter = QPainter(art)
    green = QColor('green')
    blue = QColor('blue')
    painter.fillRect(0, 0, 450, 1000, green)
    painter.fillRect(450, 0, 450, 1000, blue)
    painter.fillRect(150, 150, 150, 150, blue)
    painter.end()

    actual, expected = pixmap_differ.start(200, 200, 'test_art_shuffler_shuffle_clues')
    outline_rect(expected, 20, 0, 60, 60, blue)
    outline_rect(expected, 20, 100, 60, 60, blue)
    outline_rect(expected, 120, 0, 60, 60, green)
    outline_rect(expected, 120, 100, 60, 60, green)
    expected.fillRect(140, 120, 20, 20, blue)

    font = expected.font()
    font.setPixelSize(12)
    expected.setFont(font)
    # noinspection PyTypeChecker
    rect = expected.boundingRect(0, 0,
                                 100, 40,
                                 Qt.AlignmentFlag.AlignLeft,
                                 'DUMBFOUNDING')
    if rect.width() > 97:
        font.setPixelSize(10)
        expected.setFont(font)

    print('rect', rect)
    expected.drawText(0, 60,
                      100, 40,
                      Qt.AlignmentFlag.AlignHCenter,
                      '(_)_ _ _ _\nDUMBFOUNDING')
    font.setPixelSize(15)
    expected.setFont(font)
    expected.drawText(100, 60,
                      100, 40,
                      Qt.AlignmentFlag.AlignHCenter,
                      '(_)_ _ _ _ _ _\nCHARLIE')
    expected.drawText(0, 160,
                      100, 40,
                      Qt.AlignmentFlag.AlignHCenter,
                      '(_)_ _ _\nBETA')
    expected.drawText(100, 160,
                      100, 40,
                      Qt.AlignmentFlag.AlignHCenter,
                      '(_)_ _ _ _\nALPHA')

    actual.end()
    clues = dict(a='(_)_ _ _ _\nALPHA',
                 b='(_)_ _ _\nBETA',
                 c='(_)_ _ _ _ _ _\nCHARLIE',
                 d='(_)_ _ _ _\nDUMBFOUNDING')
    shuffler = ArtShuffler(2, 2, actual.device(), clues=clues)

    shuffler.shuffle()
    shuffler.draw(art)

    pixmap_differ.max_diff = 51
    pixmap_differ.assert_equal()


# noinspection DuplicatedCode
def test_art_shuffler_sort(pixmap_differ):
    art = QPixmap(1000, 1000)
    painter = QPainter(art)
    green = QColor('green')
    blue = QColor('blue')
    painter.fillRect(0, 0, 500, 1000, green)
    painter.fillRect(500, 0, 500, 1000, blue)
    painter.end()

    actual, expected = pixmap_differ.start(200, 200, 'art_shuffler_sort')
    outline_rect(expected, 5, 0, 90, 90, green, pen_width=3)
    outline_rect(expected, 5, 100, 90, 90, green, pen_width=3)
    outline_rect(expected, 105, 0, 90, 90, blue, pen_width=3)
    outline_rect(expected, 105, 100, 90, 90, blue, pen_width=3)

    actual.end()
    shuffler = ArtShuffler(2, 2, actual.device())
    shuffler.shuffle()
    shuffler.sort()

    shuffler.draw(art)

    pixmap_differ.assert_equal()


# noinspection DuplicatedCode
def test_art_shuffler_grid(pixmap_differ):
    art = QPixmap(1000, 1000)  # Only shape matters.

    actual, expected = pixmap_differ.start(200, 200, 'art_shuffler_grid')
    font = expected.font()
    font.setPixelSize(16)
    expected.setFont(font)
    expected.drawText(16, 0, 56, 16, Qt.AlignmentFlag.AlignCenter, 'A')
    expected.drawText(72, 0, 56, 16, Qt.AlignmentFlag.AlignCenter, 'B')
    expected.drawText(128, 0, 56, 16, Qt.AlignmentFlag.AlignCenter, 'C')
    expected.drawText(0, 72, 16, 56, Qt.AlignmentFlag.AlignCenter, 'D')
    expected.drawText(184, 72, 16, 56, Qt.AlignmentFlag.AlignCenter, 'F')
    expected.drawText(16, 184, 56, 16, Qt.AlignmentFlag.AlignCenter, 'G')
    expected.drawText(72, 184, 56, 16, Qt.AlignmentFlag.AlignCenter, 'H')
    expected.drawText(128, 184, 56, 16, Qt.AlignmentFlag.AlignCenter, 'I')
    grey_pen = QPen(QColor('lightgrey'))
    expected.setPen(grey_pen)

    expected.drawRect(16, 16, 168, 168)
    expected.drawLine(16, 72, 184, 72)
    expected.drawLine(16, 128, 184, 128)
    expected.drawLine(72, 16, 72, 184)
    expected.drawLine(128, 16, 128, 184)

    actual.end()
    shuffler = ArtShuffler(3, 3, actual.device())
    shuffler.shuffle()
    shuffler.sort()

    shuffler.draw_grid(art)

    pixmap_differ.assert_equal()


# noinspection DuplicatedCode
def test_symbols(pixmap_differ, symbol_clues, monkeypatch):
    monkeypatch.setattr('sliced_art.art_shuffler.shuffle',
                        lambda a: a.reverse())

    transparent = QColor(255, 255, 255, 0)
    blue = QColor('blue')

    art = QPixmap(900, 900)
    art.fill(transparent)
    painter = QPainter(art)
    painter.setBrush(QBrush(blue))
    painter.drawEllipse(0, 0, 900, 900)
    painter.end()

    row_clues, column_clues = symbol_clues

    actual, expected = pixmap_differ.start(200, 200, 'test_art_shuffler_symbols')
    outline_rect(expected, 5, 0, 90, 90, transparent, pen_width=3)
    expected.drawPixmap(5, 0, 90, 90, row_clues[1])
    expected.drawPixmap(5, 0, 90, 90, column_clues[1])
    expected.drawPixmap(5, 0, 90, 90,
                        art,
                        450, 450, 450, 450)
    outline_rect(expected, 5, 100, 90, 90, transparent, pen_width=3)
    expected.drawPixmap(5, 100, 90, 90, row_clues[0])
    expected.drawPixmap(5, 100, 90, 90, column_clues[1])
    expected.drawPixmap(5, 100, 90, 90,
                        art,
                        450, 0, 450, 450)
    outline_rect(expected, 105, 0, 90, 90, transparent, pen_width=3)
    expected.drawPixmap(105, 0, 90, 90, row_clues[1])
    expected.drawPixmap(105, 0, 90, 90, column_clues[0])
    expected.drawPixmap(105, 0, 90, 90,
                        art,
                        0, 450, 450, 450)
    outline_rect(expected, 105, 100, 90, 90, transparent, pen_width=3)
    expected.drawPixmap(105, 100, 90, 90, row_clues[0])
    expected.drawPixmap(105, 100, 90, 90, column_clues[0])
    expected.drawPixmap(105, 100, 90, 90,
                        art,
                        0, 0, 450, 450)

    font = expected.font()
    font.setPixelSize(15)
    expected.setFont(font)

    actual.end()
    shuffler = ArtShuffler(2,
                           2,
                           actual.device(),
                           row_clues=row_clues,
                           column_clues=column_clues)

    shuffler.shuffle()
    shuffler.draw(art)

    pixmap_differ.assert_equal()


# noinspection DuplicatedCode
def test_draw_grid_with_symbols(pixmap_differ, symbol_clues, monkeypatch):
    monkeypatch.setattr('sliced_art.art_shuffler.shuffle',
                        lambda a: a.reverse())

    transparent = QColor(255, 255, 255, 0)
    blue = QColor('blue')

    art = QPixmap(900, 900)
    art.fill(transparent)
    painter = QPainter(art)
    painter.setBrush(QBrush(blue))
    painter.end()

    row_clues, column_clues = symbol_clues

    actual, expected = pixmap_differ.start(
        180, 180,
        'test_art_shuffler_draw_grid_with_symbols')
    expected.drawPixmap(60, 1, 59, 59, column_clues[0])
    expected.drawPixmap(120, 1, 59, 59, column_clues[1])
    expected.drawPixmap(1, 60, 59, 59, row_clues[0])
    expected.drawPixmap(1, 120, 59, 59, row_clues[1])
    grey_pen = QPen(QColor('lightgrey'))
    expected.setPen(grey_pen)

    expected.drawLine(60, 1, 179, 1)
    expected.drawLine(1, 60, 179, 60)
    expected.drawLine(1, 120, 179, 120)
    expected.drawLine(1, 179, 179, 179)
    expected.drawLine(1, 60, 1, 179)
    expected.drawLine(60, 1, 60, 179)
    expected.drawLine(120, 1, 120, 179)
    expected.drawLine(179, 1, 179, 179)

    actual.end()
    shuffler = ArtShuffler(2,
                           2,
                           actual.device(),
                           row_clues=row_clues,
                           column_clues=column_clues)

    shuffler.shuffle()
    shuffler.draw_grid(art)

    pixmap_differ.assert_equal()
