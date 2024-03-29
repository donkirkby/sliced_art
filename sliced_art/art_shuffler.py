import typing
from random import shuffle

from PySide6.QtCore import QRect, Qt, QPoint
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
        self.row_clue_rects: typing.List[QRect] = []
        self.column_clue_rects: typing.List[QRect] = []
        self.background = QColor('white')
        self.selected_row = self.selected_column = None

    def draw_grid(self, art: QPixmap, painter: typing.Optional[QPainter] = None):
        rows = self.rows
        columns = self.cols
        if self.row_clues:
            x_filled_portion = 0.97 * rows / (rows+1)
            y_filled_portion = 0.97 * columns / (columns+1)
            scaled_art = art.scaled(self.rect.width()*x_filled_portion,
                                    self.rect.height()*y_filled_portion,
                                    Qt.AspectRatioMode.KeepAspectRatio)
        else:
            filled_portion = 0.84
            scaled_art = art.scaled(self.rect.width()*filled_portion,
                                    self.rect.height()*filled_portion,
                                    Qt.AspectRatioMode.KeepAspectRatio)
        cell_height = scaled_art.height() / rows
        cell_width = scaled_art.width() / columns
        if self.row_clues:
            left_clue_border = round((self.rect.width() -
                                      scaled_art.width() -
                                      cell_width) / 3)
            top_clue_border = round((self.rect.height() -
                                     scaled_art.height() -
                                     cell_height) / 3)
            min_border = min(left_clue_border, top_clue_border)
            left_clue_border = round((3*left_clue_border - min_border) / 2)
            top_clue_border = round((3*top_clue_border - min_border) / 2)
            left_border = left_clue_border + cell_width + min_border
            top_border = top_clue_border + cell_height + min_border
        else:
            left_border = int((self.rect.width()-scaled_art.width()) / 2)
            top_border = int((self.rect.height()-scaled_art.height()) / 2)
            left_clue_border = top_clue_border = None
        if painter is None:
            painter = QPainter(self.target)
        if self.background:
            painter.fillRect(self.rect, self.background)
        painter.translate(0, self.rect.top())
        if not self.row_clues:
            self.draw_letters(cell_width,
                              cell_height,
                              left_border,
                              top_border,
                              painter)
        is_grid_filled = (self.selected_row is not None or
                          self.selected_column is not None)
        self.row_clue_rects.clear()
        for i, clue in enumerate(self.row_clues):
            clue_rect = QRect(left_clue_border,
                              round(top_border + i * cell_height),
                              round(cell_width),
                              round(cell_height))
            self.row_clue_rects.append(clue_rect)
            painter.drawPixmap(clue_rect, clue)
            if is_grid_filled:
                for j in range(self.cols):
                    painter.drawPixmap(round(left_border + j * cell_width), round(top_border + i * cell_height),
                                       round(cell_width), round(cell_height),
                                       clue)
        self.column_clue_rects.clear()
        for j, clue in enumerate(self.column_clues):
            clue_rect = QRect(round(left_border + j * cell_width),
                              top_clue_border,
                              round(cell_width),
                              round(cell_height))
            self.column_clue_rects.append(clue_rect)
            painter.drawPixmap(clue_rect, clue)
            if is_grid_filled:
                for i in range(self.rows):
                    y = round(top_border + i*cell_height)
                    painter.drawPixmap(round(left_border + j * cell_width), y,
                                       round(cell_width), round(cell_height),
                                       clue)
        if is_grid_filled:
            painter.drawPixmap(left_border,
                               top_border,
                               round(self.cols*cell_width),
                               round(self.rows*cell_height),
                               scaled_art)
        painter.setPen(QPen(QColor('lightgrey'), round(cell_width / 50)))
        if self.row_clues:
            painter.drawRect(left_clue_border, top_border,
                             round(cell_width), round(cell_height * rows))
            painter.drawRect(left_border, top_clue_border,
                             round(cell_width*columns), round(cell_height))
        painter.drawRect(left_border, top_border,
                         round(cell_width * columns),
                         round(cell_height * rows))
        for i in range(1, rows):
            y = round(top_border + i*cell_height)
            painter.drawLine(left_border, y,
                             round(left_border + cell_width*columns), y)
            if self.row_clues:
                painter.drawLine(left_clue_border, y,
                                 round(left_clue_border + cell_width), y)
        for j in range(1, columns):
            x = round(left_border + j*cell_width)
            painter.drawLine(
                x, top_border,
                x, round(top_border + cell_height*rows))
            if self.row_clues:
                painter.drawLine(x, top_clue_border,
                                 x, round(top_clue_border + cell_height))

        painter.setPen(QPen(QColor('blue'), round(cell_width / 25)))
        if self.selected_row is not None:
            painter.drawRect(left_clue_border,
                             round(top_border + cell_height*self.selected_row),
                             round(cell_width), round(cell_height))
        if self.selected_column is not None:
            painter.drawRect(round(left_border + cell_width*self.selected_column),
                             top_clue_border,
                             round(cell_width), round(cell_height))
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

    def select_clue(self, point: QPoint):
        for i, clue_rect in enumerate(self.row_clue_rects):
            if clue_rect.contains(point):
                self.selected_row = i
                self.selected_column = None
                return

        for j, clue_rect in enumerate(self.column_clue_rects):
            if clue_rect.contains(point):
                self.selected_row = None
                self.selected_column = j
                return
