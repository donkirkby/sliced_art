from random import shuffle

from PySide2.QtCore import QRect, Qt
from PySide2.QtGui import QPainter, QPaintDevice, QPixmap, QColor


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

    def draw(self, art: QPixmap):
        filled_portion = 0.7 if self.is_shuffled else 0.9
        scaled_art = art.scaled(self.rect.width()*filled_portion,
                                self.rect.height()*filled_portion,
                                Qt.AspectRatioMode.KeepAspectRatio)
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
        font.setPixelSize(padding/2.1)
        painter.setFont(font)
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
