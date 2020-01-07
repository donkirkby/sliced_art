from PySide2.QtCore import QRect
from PySide2.QtGui import QPainter, QPaintDevice, QPixmap


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

    def draw(self, art: QPixmap):
        filled_portion = 0.9
        scaled_art = art.scaled(self.rect.width()*filled_portion,
                                self.rect.height()*filled_portion)
        painter = QPainter(self.target)
        row_height = self.rect.height() / self.rows
        cell_height = row_height * filled_portion
        vertical_padding = self.rect.height() - self.rows * cell_height
        row_padding = vertical_padding / (self.rows - 1)
        col_width = self.rect.width() / self.cols
        cell_width = col_width * filled_portion
        horizontal_padding = self.rect.width() - self.cols * cell_width
        col_padding = horizontal_padding / (self.cols - 1)
        padding = min(row_padding, col_padding)
        left_border = (self.cols-1) * (col_padding-padding) / 2
        top_border = (self.rows-1) * (row_padding-padding) / 2
        y = top_border
        sy = 0
        for i in range(self.rows):
            x = left_border
            sx = 0
            for j in range(self.cols):
                painter.drawPixmap(x, y, cell_width, cell_height,
                                   scaled_art,
                                   sx, sy, cell_width, cell_height)

                x += cell_width + padding
                sx += cell_width

            y += cell_height + padding
            sy += cell_height
