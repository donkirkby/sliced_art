from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsSceneMouseEvent


class ClickablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(self.ItemIsSelectable, True)
        self.on_click = lambda event: None

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.on_click(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        pass
