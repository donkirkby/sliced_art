import os
import sys
import typing
from enum import Enum
from functools import partial
from pathlib import Path

from PySide6.QtCore import Qt, QSize, QSettings, QCoreApplication, QRect, QTimer
from PySide6.QtGui import QImageReader, QPixmap, QResizeEvent, QPdfWriter, \
    QPainter, QImage, QPaintDevice, QPageSize
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, \
    QFileDialog, QGraphicsPixmapItem, QLabel, QGridLayout, QLineEdit

from sliced_art.art_shuffler import ArtShuffler
from sliced_art.main_window import Ui_MainWindow
from sliced_art.selection_grid import SelectionGrid
from sliced_art.word_shuffler import WordShuffler
from sliced_art.word_stripper import WordStripper

QCoreApplication.setOrganizationDomain("donkirkby.github.io")
QCoreApplication.setOrganizationName("Don Kirkby")
QCoreApplication.setApplicationName("Sliced Art")

ClueType = Enum('ClueType', 'words symbols')


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
        self.ui.action_save_png.triggered.connect(self.save_png)
        self.ui.action_shuffle.triggered.connect(self.shuffle)
        self.ui.action_sort.triggered.connect(self.sort)
        self.ui.rows.valueChanged.connect(self.on_options_changed)
        self.ui.columns.valueChanged.connect(self.on_options_changed)
        self.ui.word_clues_radio.toggled.connect(self.on_options_changed)
        self.ui.symbol_clues_radio.toggled.connect(self.on_options_changed)

        self.word_layout = QGridLayout(self.ui.word_content)
        self.ui.word_scroll.setWidgetResizable(True)
        self.word_labels: typing.Dict[str, QLabel] = {}
        self.word_shuffler = WordShuffler([])

        self.clues = None

        self.pixmap = self.scaled_pixmap = self.mini_pixmap = None
        self.sliced_pixmap_item: typing.Optional[QGraphicsPixmapItem] = None
        self.sliced_image: typing.Optional[QImage] = None
        self.selection_grid: typing.Optional[SelectionGrid] = None
        self.cells = []
        self.art_shuffler: typing.Optional[ArtShuffler] = None
        self.settings = QSettings()
        self.image_path: typing.Optional[str] = self.settings.value('image_path')
        self.words_path: typing.Optional[str] = self.settings.value('words_path')

        self.dirty_letters = set()
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.setSingleShot(True)
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.on_dirty)

        self.row_count = self.column_count = 0
        self.clue_type = ClueType.words
        self.ui.rows.setValue(self.settings.value('row_count', 6, int))
        self.ui.columns.setValue(self.settings.value('column_count', 4, int))
        clue_type_name = self.settings.value('clue_type', ClueType.words.name)
        try:
            clue_type = ClueType[clue_type_name]
        except KeyError:
            clue_type = ClueType.words
        if clue_type == ClueType.words:
            self.ui.word_clues_radio.setChecked(True)
        else:
            self.ui.symbol_clues_radio.setChecked(True)
        self.row_clues: typing.List[QPixmap] = []
        self.column_clues: typing.List[QPixmap] = []
        self.on_options_changed()

    def on_dirty(self):
        for letter in self.dirty_letters:
            self.word_labels[letter].setText(
                self.word_shuffler.make_display(letter))
            self.settings.setValue(f'word_{letter}', self.word_shuffler[letter])
        if self.dirty_letters:
            self.clues = self.word_shuffler.make_clues()
            self.art_shuffler.clues = dict(self.clues)
            self.dirty_letters.clear()
            self.on_selection_moved()

        if self.pixmap is not None:
            x, y, width, height = self.get_selected_fraction()
            self.settings.setValue('x', x)
            self.settings.setValue('y', y)
            self.settings.setValue('width', width)
            self.settings.setValue('height', height)

        new_rows = self.ui.rows.value()
        new_columns = self.ui.columns.value()
        if self.ui.word_clues_radio.isChecked():
            new_clue_type = ClueType.words
        else:
            new_clue_type = ClueType.symbols
        if (new_rows,
            new_columns,
            new_clue_type) == (self.row_count,
                               self.column_count,
                               self.clue_type):
            return
        self.settings.setValue('row_count', new_rows)
        self.settings.setValue('column_count', new_columns)
        self.settings.setValue('clue_type', new_clue_type.name)
        self.row_count, self.column_count = new_rows, new_columns
        self.clue_type = new_clue_type

        word_count = (self.row_count * self.column_count)
        while self.word_layout.count():
            layout_item = self.word_layout.takeAt(0)
            layout_item.widget().deleteLater()
        self.word_labels.clear()

        self.row_clues.clear()
        self.column_clues.clear()
        if self.image_path is not None:
            image_folder = Path(self.image_path).parent
            if new_clue_type == ClueType.symbols:
                for i in range(new_rows):
                    clue_path = image_folder / f'row{i}.png'
                    clue_image = QPixmap(str(clue_path))
                    if not clue_image.isNull():
                        self.row_clues.append(clue_image)
                for j in range(new_columns):
                    clue_path = image_folder / f'col{j}.png'
                    clue_image = QPixmap(str(clue_path))
                    if not clue_image.isNull():
                        self.column_clues.append(clue_image)
                if (len(self.row_clues) != new_rows or
                        len(self.column_clues) != new_columns):
                    self.row_clues.clear()
                    self.column_clues.clear()
            self.load_image(self.image_path)

        if self.words_path is not None:
            self.load_words(self.words_path)

        letters = [chr(65+i) for i in range(word_count)]
        if self.word_shuffler.needs_blank:
            letters.insert(0, '')
        word_fields = {}
        for i, letter in enumerate(letters):
            word_field = QLineEdit()
            self.word_layout.addWidget(word_field, i, 0)
            # noinspection PyUnresolvedReferences
            word_field.textEdited.connect(partial(self.on_word_edited, letter))

            word_label = QLabel()
            self.word_layout.addWidget(word_label, i, 1)
            self.word_labels[letter] = word_label
            word_fields[letter] = word_field
        for i, letter in enumerate(letters):
            word = self.settings.value(f'word_{letter}', '')
            self.word_shuffler[letter] = word
            self.dirty_letters.add(letter)
            word_fields[letter].setText(word)

    def on_options_changed(self, *_):
        self.timer.start()

    def shuffle(self):
        self.clues = self.word_shuffler.make_clues()
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
            filter=word_filter)
        if not file_name:
            return
        self.settings.setValue('words_path', file_name)
        self.load_words(file_name)

    def load_words(self, words_path):
        with open(words_path) as f:
            choice = 0
            if choice == 0:
                self.word_shuffler = WordShuffler(f)
            else:
                self.word_shuffler = WordStripper(f)

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
            filter=image_filter)
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
            x = self.settings.value('x', 0.0, float)
            y = self.settings.value('y', 0.0, float)
            width = self.settings.value('width', 1.0, float)
            height = self.settings.value('height', 1.0, float)
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
        self.check_clues()
        self.art_shuffler = ArtShuffler(self.selection_grid.row_count,
                                        self.selection_grid.column_count,
                                        self.sliced_image,
                                        QRect(0,
                                              0,
                                              display_size.width(),
                                              display_size.height()),
                                        clues=self.clues,
                                        row_clues=self.row_clues,
                                        column_clues=self.column_clues)
        self.sliced_pixmap_item = self.scene.addPixmap(
            QPixmap.fromImage(self.sliced_image))
        self.sliced_pixmap_item.setPos(display_size.width(), 0)
        self.on_selection_moved()

    def on_word_edited(self, letter, word):
        self.word_shuffler[letter] = word
        self.dirty_letters.add(letter)
        self.timer.start()

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
        self.timer.start()

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
            filter='Documents (*.pdf)')
        if not file_name:
            return
        self.settings.setValue('pdf_folder', os.path.dirname(file_name))
        writer = QPdfWriter(file_name)
        writer.setPageSize(QPageSize(QPageSize.Letter))
        writer.setTitle('Sliced Art Puzzle')
        writer.setCreator('Don Kirkby')
        self.paint_puzzle(writer)

    def save_png(self):
        pdf_folder = self.settings.value('pdf_folder')
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save an image file.",
            dir=pdf_folder,
            filter='Images (*.png)')
        if not file_name:
            return
        writer = QPixmap(1000, 2000)
        self.paint_puzzle(writer)
        writer.save(file_name)
        self.settings.setValue('pdf_folder', os.path.dirname(file_name))

    def paint_puzzle(self, writer: QPaintDevice):
        self.check_clues()
        painter = QPainter(writer)
        try:
            print_shuffler = ArtShuffler(self.art_shuffler.rows,
                                         self.art_shuffler.cols,
                                         writer,
                                         QRect(0, 0,
                                               writer.width(),
                                               round(writer.height()/2)),
                                         clues=self.clues,
                                         row_clues=self.row_clues,
                                         column_clues=self.column_clues)
            print_shuffler.cells = self.art_shuffler.cells[:]
            print_shuffler.is_shuffled = self.art_shuffler.is_shuffled
            selected_pixmap = self.get_selected_pixmap()
            print_shuffler.draw(selected_pixmap, painter)

            print_shuffler.rect.moveTop(writer.height()/2)
            print_shuffler.draw_grid(selected_pixmap, painter)
        finally:
            painter.end()

    def check_clues(self):
        if self.clue_type == ClueType.words:
            if self.clues is None:
                self.clues = self.word_shuffler.make_clues()
            self.row_clues.clear()
            self.column_clues.clear()
        else:
            self.clues = None


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
