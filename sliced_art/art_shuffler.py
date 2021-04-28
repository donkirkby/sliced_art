import typing
from random import shuffle

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QPainter, QPaintDevice, QPixmap, QColor, QPen


class ArtShuffler:
    def __init__(self,
                 rows: int,
                 cols: int,
                 target: QPaintDevice,
                 rect: QRect = None,
                 clues: typing.Dict[str, str] = None,
                 row_clues: typing.Iterable[QPixmap] = None,
                 column_clues: typing.Iterable[QPixmap] = None):
        """ Initialize the object.

        :param rows: the number of rows to break the art into
        :param cols: the number of columns to break the art into
        :param target: what to paint the pieces on
        :param rect: where to paint the pieces, or None to use the full target
        :param clues: word clues to display, defaults to just the letters
        :param row_clues: one image to use as a clue for each row
        :param column_clues: one image to use as a clue for each column
        """
        self.rows = rows
        self.cols = cols
        self.target = target
        self.rect = rect or QRect(0, 0, target.width(), target.height())
        self.cells = [(i, j, chr(65+k))
                      for k, (i, j) in enumerate((i, j)
                                                 for i in range(rows)
                                                 for j in range(cols))]
        self.is_shuffled = False
        self.clues = clues or {}
        self.row_clues = [] if row_clues is None else list(row_clues)
        self.column_clues = [] if column_clues is None else list(column_clues)

    def draw_grid(self, art: QPixmap, painter: typing.Optional[QPainter] = None):
        rows = self.rows
        columns = self.cols
        if self.row_clues:
            filled_portion = 0.99
            rows += 1
            columns += 1
        else:
            filled_portion = 0.84
        scaled_art = art.scaled(self.rect.width()*filled_portion,
                                self.rect.height()*filled_portion,
                                Qt.AspectRatioMode.KeepAspectRatio)
        cell_height = scaled_art.height() / rows
        cell_width = scaled_art.width() / columns
        left_border = int((self.rect.width()-scaled_art.width()) / 2)
        top_border = int((self.rect.height()-scaled_art.height()) / 2)
        if painter is None:
            painter = QPainter(self.target)
        painter.fillRect(self.rect, QColor('white'))
        painter.translate(0, self.rect.top())
        if not self.row_clues:
            self.draw_letters(cell_width,
                              cell_height,
                              left_border,
                              top_border,
                              painter)
        for i, clue in enumerate(self.row_clues, 1):
            y = round(top_border + i*cell_height)
            x = left_border
            painter.drawPixmap(x, y,
                               round(cell_width), round(cell_height),
                               clue)
        for j, clue in enumerate(self.column_clues, 1):
            x = round(left_border + j*cell_width)
            y = top_border
            painter.drawPixmap(x, y,
                               round(cell_width), round(cell_height),
                               clue)
        pen = QPen(QColor('lightgrey'))
        painter.setPen(pen)
        for i in range(rows+1):
            y = round(top_border + i*cell_height)
            x = left_border
            if self.row_clues and i == 0:
                x += cell_width
            painter.drawLine(x, y, left_border+scaled_art.width(), y)
        for j in range(columns+1):
            x = round(left_border + j*cell_width)
            y = top_border
            if self.row_clues and j == 0:
                y += cell_height
            painter.drawLine(x, y, x, top_border+scaled_art.height())
        painter.translate(0, -self.rect.top())

    def draw_letters(self,
                     cell_width: float,
                     cell_height: float,
                     left_border: int,
                     top_border: int,
                     painter: QPainter):
        font = painter.font()
        font_size = round(top_border * 0.99)
        font.setPixelSize(font_size)
        painter.setFont(font)
        ascii_code = ord('A')
        for i in range(self.rows):
            for j in range(self.cols):
                letter = chr(ascii_code)
                x = round(left_border + j * cell_width)
                y = round(top_border + i * cell_height)
                w = round(cell_width)
                h = round(cell_height)
                if i == 0:
                    y = top_border - font_size
                    h = font_size
                elif i == self.rows - 1:
                    y = self.rect.height() - top_border
                    h = font_size
                elif j == 0:
                    x = left_border - font_size
                    w = font_size
                elif j == self.cols - 1:
                    x = self.rect.width() - left_border
                    w = font_size
                else:
                    x = y = w = h = 0
                if w != 0:
                    painter.drawText(x, y,
                                     w, h,
                                     Qt.AlignmentFlag.AlignCenter,
                                     letter)
                ascii_code += 1

    def draw(self, art: QPixmap, painter: typing.Optional[QPainter] = None):
        filled_portion = 0.6 if self.is_shuffled and not self.row_clues else 0.9
        scaled_art = art.scaled(self.rect.width()*filled_portion,
                                self.rect.height()*filled_portion,
                                Qt.AspectRatioMode.KeepAspectRatio)
        if painter is None:
            painter = QPainter(self.target)
        painter.fillRect(self.rect, QColor('white'))
        cell_height = round(scaled_art.height() / self.rows)
        vertical_padding = self.rect.height() - self.rows * cell_height
        row_padding = vertical_padding / self.rows
        cell_width = round(scaled_art.width() / self.cols)
        horizontal_padding = self.rect.width() - self.cols * cell_width
        col_padding = horizontal_padding / self.cols
        padding = min(row_padding, col_padding)
        left_border = self.cols * (col_padding - padding) / 2
        top_border = self.rows * (row_padding - padding) / 2
        font = painter.font()
        font.setPixelSize(padding/2.6)
        painter.setFont(font)
        old_pen = painter.pen()
        grey_pen = QPen(QColor('lightgrey'))
        width = max(cell_width/35, 2)
        grey_pen.setWidth(round(width))
        y = top_border
        cell_index = 0
        for i in range(self.rows):
            x = left_border
            for j in range(self.cols):
                si, sj, label = self.cells[cell_index]
                clue = self.clues.get(label.lower(), label)
                sx = sj * cell_width
                sy = si * cell_height
                painter.setPen(grey_pen)
                painter.drawRect(x+padding/2, y,
                                 cell_width, cell_height)
                painter.setPen(old_pen)
                if self.is_shuffled:
                    original_size = new_size = font.pixelSize()
                    while True:
                        # noinspection PyTypeChecker
                        rect = painter.boundingRect(0, 0,
                                                    cell_width, padding,
                                                    Qt.AlignmentFlag.AlignLeft,
                                                    clue)
                        if (rect.width() <= cell_width + padding and
                                rect.height() <= padding):
                            break
                        new_size *= 0.9
                        font.setPixelSize(new_size)
                        painter.setFont(font)
                    if not self.row_clues:
                        painter.drawText(x, y+cell_height,
                                         cell_width + padding, padding,
                                         Qt.AlignmentFlag.AlignHCenter, clue)
                    else:
                        painter.drawPixmap(x + padding / 2, y,
                                           cell_width, cell_height,
                                           self.row_clues[si],
                                           0, 0,
                                           0, 0)
                        painter.drawPixmap(x + padding / 2, y,
                                           cell_width, cell_height,
                                           self.column_clues[sj],
                                           0, 0,
                                           0, 0)
                    font.setPixelSize(original_size)
                    painter.setFont(font)
                painter.drawPixmap(x+padding/2, y,
                                   cell_width, cell_height,
                                   scaled_art,
                                   sx, sy,
                                   cell_width, cell_height)

                x += cell_width + padding
                cell_index += 1

            y += cell_height + padding

    def shuffle(self):
        shuffle(self.cells)
        self.is_shuffled = True

    def sort(self):
        self.cells.sort()
        self.is_shuffled = False
