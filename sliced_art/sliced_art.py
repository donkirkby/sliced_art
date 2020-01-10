import os
import sys
import typing

from PySide2.QtCore import Qt, QSize, QSettings, QCoreApplication, QRect
from PySide2.QtGui import QImageReader, QPixmap, QResizeEvent, QPdfWriter, QPainter, QImage
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QFileDialog, QGraphicsPixmapItem

from sliced_art.art_shuffler import ArtShuffler
from sliced_art.main_window import Ui_MainWindow
from sliced_art.selection_grid import SelectionGrid

QCoreApplication.setOrganizationDomain("donkirkby.github.io")
QCoreApplication.setOrganizationName("Don Kirkby")
QCoreApplication.setApplicationName("Sliced Art")


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
        self.ui.actionSave.triggered.connect(self.save_pdf)
        self.ui.actionShuffle.triggered.connect(self.shuffle)
        self.ui.actionSort.triggered.connect(self.sort)

        self.pixmap = self.scaled_pixmap = self.mini_pixmap = None
        self.sliced_pixmap_item: typing.Optional[QGraphicsPixmapItem] = None
        self.sliced_image: typing.Optional[QImage] = None
        self.selection_grid: typing.Optional[SelectionGrid] = None
        self.cells = []
        self.settings = QSettings()
        self.art_shuffler: typing.Optional[ArtShuffler] = None

    def shuffle(self):
        if self.art_shuffler is not None:
            self.art_shuffler.shuffle()
            self.on_selection_moved()

    def sort(self):
        if self.art_shuffler is not None:
            self.art_shuffler.sort()
            self.on_selection_moved()

    def open_image(self):
        formats = QImageReader.supportedImageFormats()
        patterns = (f'*.{fmt.data().decode()}' for fmt in formats)
        image_filter = f'Images ({" ".join(patterns)})'
        image_folder = self.settings.value('image_folder')
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open an image file.",
            dir=image_folder,
            filter=image_filter,
            options=QFileDialog.DontUseNativeDialog)
        if not file_name:
            return
        self.settings.setValue('image_folder', os.path.dirname(file_name))
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
        self.sliced_image = QImage(display_size,
                                   QImage.Format.Format_ARGB32_Premultiplied)
        self.art_shuffler = ArtShuffler(self.selection_grid.row_count,
                                        self.selection_grid.column_count,
                                        self.sliced_image,
                                        QRect(0,
                                              0,
                                              display_size.width(),
                                              display_size.height()))
        self.sliced_pixmap_item = self.scene.addPixmap(
            QPixmap.fromImage(self.sliced_image))
        self.sliced_pixmap_item.setPos(display_size.width(), 0)
        self.on_selection_moved()

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
        self.draw_selected(self.art_shuffler)
        self.sliced_pixmap_item.setPixmap(QPixmap.fromImage(self.sliced_image))

    def draw_selected(self, shuffler):
        x, y, width, height = self.get_selected_fraction()
        original_size = self.pixmap.size()
        selected_pixmap = self.pixmap.copy(x * original_size.width(),
                                           y * original_size.height(),
                                           width * original_size.width(),
                                           height * original_size.height())
        shuffler.draw(selected_pixmap)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.scale_image()

    def save_pdf(self):
        pdf_folder = self.settings.value('pdf_folder')
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save a PDF file.",
            dir=pdf_folder,
            filter='Documents (*.pdf)',
            options=QFileDialog.DontUseNativeDialog)
        if not file_name:
            return
        self.settings.setValue('pdf_folder', os.path.dirname(file_name))
        writer = QPdfWriter(file_name)
        p = QPainter()
        p.begin(writer)
        try:
            p.drawText(0, 0, 'Hello, World!')
        finally:
            p.end()
        print_shuffler = ArtShuffler(self.art_shuffler.rows,
                                     self.art_shuffler.cols,
                                     writer,
                                     QRect(0, 0,
                                           writer.width(), writer.height()/2))
        print_shuffler.cells = self.art_shuffler.cells[:]
        print_shuffler.is_shuffled = self.art_shuffler.is_shuffled
        self.draw_selected(print_shuffler)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
