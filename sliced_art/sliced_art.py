import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QImageReader, QPixmap, QResizeEvent
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QFileDialog

from sliced_art.main_window import Ui_MainWindow


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

        self.pixmap = None

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

        self.scene.clear()
        view_size = self.ui.graphicsView.maximumViewportSize()
        scaled = self.pixmap.scaled(view_size,
                                    aspectMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.scene.addPixmap(scaled)

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
