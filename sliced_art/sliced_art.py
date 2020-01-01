import sys

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QImageReader, QPixmap, QResizeEvent
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QFileDialog

from sliced_art.main_window import Ui_MainWindow
from sliced_art.selection_grid import SelectionGrid


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scene = QGraphicsScene(self)
        self.scene.addText('Open an image file.')
        self.ui.graphicsView.setScene(self.scene)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionOpen.triggered.connect(self.open_image)

        self.pixmap = self.scaled_pixmap = self.mini_pixmap = None
        self.selection_grid = None
        self.cells = []

    def open_image(self):
        formats = QImageReader.supportedImageFormats()
        patterns = (f'*.{fmt.data().decode()}' for fmt in formats)
        image_filter = f'Images ({" ".join(patterns)})'
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open an image file.",
            filter=image_filter,
            options=QFileDialog.DontUseNativeDialog)
        self.pixmap = QPixmap(file_name)
        self.scale_image()

    def scale_image(self):
        if self.pixmap is None:
            return

        if self.selection_grid is None:
            x = y = 0
            width = height = 1
        else:
            x, y, width, height = self.get_selected_fraction()
        self.scene.clear()
        self.cells.clear()
        view_size = self.ui.graphicsView.maximumViewportSize()
        display_size = QSize(view_size.width() * 0.99 / 2,
                             view_size.height() * 0.99)
        self.scaled_pixmap = self.pixmap.scaled(
            display_size,
            aspectMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.scene.addPixmap(self.scaled_pixmap)
        scaled_size = self.scaled_pixmap.size()
        self.selection_grid = SelectionGrid(scaled_size.width()*x,
                                            scaled_size.height()*y,
                                            scaled_size.width()*width,
                                            scaled_size.height()*height)
        self.selection_grid.on_moved = self.on_selection_moved
        self.scene.addItem(self.selection_grid)
        self.on_selection_moved()
        self.scene.addRect(scaled_size.width(),
                           0,
                           scaled_size.width(),
                           scaled_size.height())

    def get_selected_fraction(self):
        selection_rect = self.selection_grid.rect()
        selection_pos = self.selection_grid.pos()
        size = self.scaled_pixmap.size()
        x = (selection_pos.x() + selection_rect.x()) / size.width()
        width = selection_rect.width() / size.width()
        y = (selection_pos.y() + selection_rect.y()) / size.height()
        height = selection_rect.height() / size.height()
        return x, y, width, height

    def on_selection_moved(self):
        mini_size = QSize(self.width()*9//20, self.height()*9//10)

        x, y, width, height = self.get_selected_fraction()
        original_size = self.pixmap.size()
        selected_pixmap = self.pixmap.copy(x*original_size.width(),
                                           y*original_size.height(),
                                           width*original_size.width(),
                                           height*original_size.height())
        selected_pixmap = selected_pixmap.scaled(
            mini_size,
            aspectMode=Qt.AspectRatioMode.KeepAspectRatio)

        if self.cells:
            pixmap_item = self.cells[0]
            pixmap_item.setPixmap(selected_pixmap)
        else:
            pixmap_item = self.scene.addPixmap(selected_pixmap)
            self.cells.append(pixmap_item)
            pixmap_item.setPos(self.width()/2, 0)

        row_count = self.selection_grid.row_count
        column_count = self.selection_grid.column_count
        rect = selected_pixmap.rect()
        cell_width = rect.width() / column_count
        cell_height = rect.height() / row_count

        for row in range(row_count):
            y = rect.top() + rect.height() * row / row_count
            for column in range(column_count):
                x = rect.left() + rect.width() * column / column_count
                i = row * column_count + column
                cell_pixmap = selected_pixmap.copy(x, y, cell_width, cell_height)
                if i >= len(self.cells):
                    pixmap_item = self.scene.addPixmap(cell_pixmap)
                    self.cells.append(pixmap_item)
                else:
                    pixmap_item = self.cells[i]
                    pixmap_item.setPixmap(cell_pixmap)
                pixmap_item.setPos(self.width()/2 + x / 0.9, y/0.9)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.scale_image()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
