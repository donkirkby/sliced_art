import typing
from random import shuffle

from PySide2.QtCore import QRect, Qt
from PySide2.QtGui import QPainter, QPaintDevice, QPixmap, QColor, QPen


class ArtShuffler:
    def __init__(self,
                 rows: int,
                 cols: int,
                 target: QPaintDevice,
                 rect: QRect = None):
        """ Initialize the object.

        :param rows: the number of rows to break the art into
        :param cols: the number of columns to break the art into
        :param target: what to paint the pieces on
        :param rect: where to paint the pieces, or None to use the full target
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

    def draw_grid(self, art: QPixmap, painter: typing.Optional[QPainter] = None):
        filled_portion = 0.9
        scaled_art = art.scaled(self.rect.width()*filled_portion,
                                self.rect.height()*filled_portion,
                                Qt.AspectRatioMode.KeepAspectRatio)
        cell_height = scaled_art.height() / self.rows
        cell_width = scaled_art.width() / self.cols
        left_border = (self.rect.width()-scaled_art.width()) / 2
        top_border = self.rect.top() + self.rect.height()*1/20
        if painter is None:
            painter = QPainter(self.target)
        painter.fillRect(self.rect, QColor('white'))
        pen = QPen(QColor('lightgrey'))
        painter.setPen(pen)
        painter.drawRect(left_border,
                         top_border,
                         scaled_art.width(),
                         scaled_art.height())
        for i in range(1, self.rows):
            y = top_border + i*cell_height
            painter.drawLine(left_border, y, left_border+scaled_art.width(), y)
        for j in range(1, self.cols):
            x = left_border + j*cell_width
            painter.drawLine(x, top_border, x, top_border+scaled_art.height())

    def draw(self, art: QPixmap, painter: typing.Optional[QPainter] = None):
        filled_portion = 0.7 if self.is_shuffled else 0.9
        scaled_art = art.scaled(self.rect.width()*filled_portion,
                                self.rect.height()*filled_portion,
                                Qt.AspectRatioMode.KeepAspectRatio)
        if painter is None:
            painter = QPainter(self.target)
        painter.fillRect(self.rect, QColor('white'))
        cell_height = scaled_art.height() / self.rows
        vertical_padding = self.rect.height() - self.rows * cell_height
        row_padding = vertical_padding / self.rows
        cell_width = scaled_art.width() / self.cols
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
        grey_pen.setWidth(width)
        y = top_border
        cell_index = 0
        for i in range(self.rows):
            x = left_border
            for j in range(self.cols):
                si, sj, label = self.cells[cell_index]
                sx = sj * cell_width
                sy = si * cell_height
                if self.is_shuffled:
                    painter.drawText(x+padding/2, y,
                                     cell_width, padding/2,
                                     Qt.AlignmentFlag.AlignHCenter, label)
                painter.setPen(grey_pen)
                painter.drawRect(x+padding/2, y+padding/2,
                                 cell_width, cell_height)
                painter.setPen(old_pen)
                painter.drawPixmap(x+padding/2, y+padding/2,
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
