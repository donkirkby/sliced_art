import sys

from PySide2.QtGui import QImageReader, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QFileDialog

from sliced_art.main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scene = QGraphicsScene(self)
        self.scene.addText('Hello, Scene!')
        self.ui.graphicsView.setScene(self.scene)
        # self.ui.start.clicked.connect(self.on_start)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionOpen.triggered.connect(self.open_image)

    def open_image(self):
        formats = QImageReader.supportedImageFormats()
        patterns = (f'*.{fmt.data().decode()}' for fmt in formats)
        image_filter = f'Images ({" ".join(patterns)})'
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open an image file.",
            filter=image_filter,
            options=QFileDialog.DontUseNativeDialog)
        pixmap = QPixmap(file_name)
        self.scene.addPixmap(pixmap)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
