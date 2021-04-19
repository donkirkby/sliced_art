import typing
from pathlib import Path
from turtle import Turtle

import pytest
from PySide2.QtCore import QByteArray, QBuffer, QIODevice, Qt
from PySide2.QtGui import QPixmap, QPainter, QColor, QImage, QPen
from PySide2.QtWidgets import QApplication

from sliced_art.art_shuffler import ArtShuffler


@pytest.fixture(scope='session')
def pixmap_differ():
    app = QApplication()

    yield PixmapDiffer()

    assert app


def encode_image(image: QImage):
    image_bytes = QByteArray()
    buffer = QBuffer(image_bytes)
    buffer.open(QIODevice.WriteOnly)
    image.save(buffer, "PNG")  # writes pixmap into bytes in PNG format
    encoded_bytes = image_bytes.toBase64()
    encoded_string = encoded_bytes.data().decode()
    return encoded_string


def display_diff(actual_image: QImage,
                 diff_image: QImage,
                 expected_image: QImage):
    # Display image when in live turtle mode.
    display_image = getattr(Turtle, 'display_image', None)
    if display_image is None:
        return
    t = Turtle()
    try:
        w = t.getscreen().window_width()
        h = t.getscreen().window_height()
        ox, oy = w / 2, h / 2
        text_height = 20
        t.penup()
        t.goto(-ox, oy)
        t.right(90)
        t.forward(text_height)
        t.write(f'Actual')
        display_image(ox + t.xcor(), oy - t.ycor(),
                      image=encode_image(actual_image))
        t.forward(actual_image.height())
        t.forward(text_height)
        t.write(f'Diff')
        display_image(ox + t.xcor(), oy - t.ycor(),
                      image=encode_image(diff_image))
        t.forward(diff_image.height())
        t.forward(text_height)
        t.write('Expected')
        display_image(ox + t.xcor(), oy - t.ycor(),
                      image=encode_image(expected_image))
        t.forward(expected_image.height())
    except Exception as ex:
        t.write(str(ex))


class PixmapDiffer:
    def __init__(self):
        self.name = None
        self.actual_pixmap = self.expected_pixmap = None
        self.actual = self.expected = None
        self.different_pixels = 0

        self.names = set()

        self.work_dir: Path = Path(__file__).parent / 'pixmap_diffs'
        self.work_dir.mkdir(exist_ok=True)
        for work_file in self.work_dir.iterdir():
            if work_file.name == '.gitignore':
                continue
            assert work_file.suffix == '.png'
            work_file.unlink()

    def start(self,
              width: int,
              height: int,
              name: str) -> typing.Tuple[QPainter, QPainter]:
        """ Create painters for the actual and expected images.

        Caller must either call end() or assert_equal() to properly clean up
        the painters and pixmaps. Caller may either paint through the returned
        painters, or call the end() method and create a new painter on the
        same device. Order matters, though!
        """
        assert name not in self.names
        self.names.add(name)
        self.name = name

        white = QColor('white')
        self.actual_pixmap = QPixmap(width, height)
        self.actual = QPainter(self.actual_pixmap)
        self.actual.fillRect(0, 0, width, height, white)
        self.expected_pixmap = QPixmap(width, height)
        self.expected = QPainter(self.expected_pixmap)
        self.expected.fillRect(0, 0, width, height, white)
        self.different_pixels = 0

        return self.actual, self.expected

    def end(self):
        if self.actual.isActive():
            self.actual.end()
        if self.expected.isActive():
            self.expected.end()

    def assert_equal(self):
        __tracebackhide__ = True
        self.end()
        actual_image: QImage = self.actual.device().toImage()
        expected_image: QImage = self.expected.device().toImage()
        diff_pixmap = QPixmap(actual_image.width(), actual_image.height())
        diff = QPainter(diff_pixmap)
        white = QColor('white')
        diff.fillRect(0, 0, actual_image.width(), actual_image.height(), white)
        for x in range(actual_image.width()):
            for y in range(actual_image.height()):
                actual_colour = actual_image.pixelColor(x, y)
                expected_colour = expected_image.pixelColor(x, y)
                diff.setPen(self.diff_colour(actual_colour, expected_colour))
                diff.drawPoint(x, y)
        diff.end()
        diff_image: QImage = diff.device().toImage()

        display_diff(actual_image, diff_image, expected_image)

        if self.different_pixels == 0:
            return
        actual_image.save(str(self.work_dir / (self.name + '_actual.png')))
        expected_image.save(str(self.work_dir / (self.name + '_expected.png')))
        diff_path = str(self.work_dir / (self.name + '_diff.png'))
        diff_image.save(diff_path)
        message = f'Found different pixels, see {diff_path}.'
        assert self.different_pixels == 0, message

    def diff_colour(self, actual_colour: QColor, expected_colour: QColor):
        if actual_colour == expected_colour:
            diff_colour = actual_colour.toRgb()
            diff_colour.setAlpha(diff_colour.alpha() // 3)
            return diff_colour
        self.different_pixels += 1
        # Colour
        dr = 0xff
        dg = (actual_colour.green() + expected_colour.green()) // 5
        db = (actual_colour.blue() + expected_colour.blue()) // 5

        # Opacity
        da = 0xff
        return QColor(dr, dg, db, da)


def outline_rect(painter, x, y, width, height, colour):
    old_pen = painter.pen()
    grey_pen = QPen(QColor('lightgrey'))
    grey_pen.setWidth(2)
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
    outline_rect(expected, 5, 0, 90, 90, green)
    outline_rect(expected, 5, 100, 90, 90, green)
    outline_rect(expected, 105, 0, 90, 90, blue)
    outline_rect(expected, 105, 100, 90, 90, blue)

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
    outline_rect(expected, 7, 0, 90, 45, green)
    outline_rect(expected, 7, 50, 90, 45, green)
    outline_rect(expected, 102, 0, 90, 45, blue)
    outline_rect(expected, 102, 50, 90, 45, blue)

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
    outline_rect(expected, 5, 0, 90, 90, green)
    outline_rect(expected, 5, 100, 90, 90, green)
    outline_rect(expected, 105, 0, 90, 90, blue)
    outline_rect(expected, 105, 100, 90, 90, blue)

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
    outline_rect(expected, 5, 0, 90, 90, green)
    outline_rect(expected, 5, 100, 90, 90, green)
    outline_rect(expected, 105, 0, 90, 90, blue)
    outline_rect(expected, 105, 100, 90, 90, blue)

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
    font.setPixelSize(15)
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
