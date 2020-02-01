import os
import sys
import typing
from functools import partial
from pathlib import Path

from PySide2.QtCore import Qt, QSize, QSettings, QCoreApplication, QRect
from PySide2.QtGui import QImageReader, QPixmap, QResizeEvent, QPdfWriter, QPainter, QImage
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, \
    QFileDialog, QGraphicsPixmapItem, QLabel, QGridLayout, QLineEdit

from sliced_art.art_shuffler import ArtShuffler
from sliced_art.main_window import Ui_MainWindow
from sliced_art.selection_grid import SelectionGrid
from sliced_art.word_shuffler import WordShuffler

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
        self.ui.graphics_view.setScene(self.scene)
        self.ui.action_exit.triggered.connect(self.close)
        self.ui.action_open_art.triggered.connect(self.open_image)
        self.ui.action_open_words.triggered.connect(self.open_words)
        self.ui.action_save.triggered.connect(self.save_pdf)
        self.ui.action_shuffle.triggered.connect(self.shuffle)
        self.ui.action_sort.triggered.connect(self.sort)

        self.word_layout = QGridLayout(self.ui.word_content)
        self.ui.word_scroll.setWidgetResizable(True)
        self.word_labels: typing.Dict[str, QLabel] = {}
        self.word_shuffler = WordShuffler([])

        self.row_count = 4
        self.column_count = 6
        word_count = (self.row_count * self.column_count)
        while self.word_layout.count():
            layout_item = self.word_layout.takeAt(0)
            layout_item.widget().deleteLater()
        self.word_labels.clear()

        word_fields = {}
        for i in range(word_count):
            letter = chr(65+i)

            word_field = QLineEdit()
            self.word_layout.addWidget(word_field, i, 0)
            # noinspection PyUnresolvedReferences
            word_field.textEdited.connect(partial(self.on_word_edited, letter))

            word_label = QLabel()
            self.word_layout.addWidget(word_label, i, 1)
            self.word_labels[letter] = word_label
            word_fields[letter] = word_field

        self.pixmap = self.scaled_pixmap = self.mini_pixmap = None
        self.sliced_pixmap_item: typing.Optional[QGraphicsPixmapItem] = None
        self.sliced_image: typing.Optional[QImage] = None
        self.selection_grid: typing.Optional[SelectionGrid] = None
        self.cells = []
        self.art_shuffler: typing.Optional[ArtShuffler] = None
        self.settings = QSettings()
        self.image_path: typing.Optional[str] = self.settings.value('image_path')
        if self.image_path is not None:
            self.load_image(self.image_path)
        self.words_path: typing.Optional[str] = self.settings.value('words_path')
        if self.words_path is not None:
            self.load_words(self.words_path)

        for i in range(word_count):
            letter = chr(65+i)
            word = self.settings.value(f'word_{letter}', '')
            self.on_word_edited(letter, word)
            word_fields[letter].setText(word)

    def shuffle(self):
        if self.art_shuffler is not None:
            self.art_shuffler.shuffle()
            self.on_selection_moved()

    def sort(self):
        if self.art_shuffler is not None:
            self.art_shuffler.sort()
            self.on_selection_moved()

    def open_words(self):
        word_filter = 'Text files (*.txt)'
        if self.words_path is None:
            words_folder = None
        else:
            words_folder = str(Path(self.words_path).parent)
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open a words file.",
            dir=words_folder,
            filter=word_filter,
            options=QFileDialog.DontUseNativeDialog)
        if not file_name:
            return
        self.settings.setValue('words_path', file_name)
        self.load_words(file_name)

    def load_words(self, words_path):
        with open(words_path) as f:
            self.word_shuffler = WordShuffler(f)

    def open_image(self):
        formats = QImageReader.supportedImageFormats()
        patterns = (f'*.{fmt.data().decode()}' for fmt in formats)
        image_filter = f'Images ({" ".join(patterns)})'
        if self.image_path is None:
            image_folder = None
        else:
            image_folder = str(Path(self.image_path).parent)
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open an image file.",
            dir=image_folder,
            filter=image_filter,
            options=QFileDialog.DontUseNativeDialog)
        if not file_name:
            return
        self.settings.setValue('image_path', file_name)
        self.load_image(file_name)

    def load_image(self, image_path):
        self.pixmap = QPixmap(image_path)
        if self.pixmap.isNull():
            self.pixmap = None
        self.image_path = image_path
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
        view_size = self.ui.graphics_view.maximumViewportSize()
        if view_size.width() == 0:
            return
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
                                            scaled_size.height()*height,
                                            row_count=self.row_count,
                                            column_count=self.column_count)
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

    def on_word_edited(self, letter, word):
        self.word_labels[letter].setText(self.word_shuffler.display(word,
                                                                    letter))
        self.settings.setValue(f'word_{letter}', word)

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
        self.art_shuffler.draw(self.get_selected_pixmap())
        self.sliced_pixmap_item.setPixmap(QPixmap.fromImage(self.sliced_image))

    def get_selected_pixmap(self) -> QPixmap:
        x, y, width, height = self.get_selected_fraction()
        original_size = self.pixmap.size()
        selected_pixmap = self.pixmap.copy(x * original_size.width(),
                                           y * original_size.height(),
                                           width * original_size.width(),
                                           height * original_size.height())
        return selected_pixmap

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
        writer.setPageSize(QPdfWriter.Letter)
        painter = QPainter(writer)
        try:
            print_shuffler = ArtShuffler(self.art_shuffler.rows,
                                         self.art_shuffler.cols,
                                         writer,
                                         QRect(0, 0,
                                               writer.width(), writer.height()/2))
            print_shuffler.cells = self.art_shuffler.cells[:]
            print_shuffler.is_shuffled = self.art_shuffler.is_shuffled
            selected_pixmap = self.get_selected_pixmap()
            print_shuffler.draw(selected_pixmap, painter)

            print_shuffler.rect.moveTop(writer.height()/2)
            print_shuffler.draw_grid(selected_pixmap, painter)
        finally:
            painter.end()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
