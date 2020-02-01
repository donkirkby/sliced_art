from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsItem


class SelectionGrid(QGraphicsRectItem):

    HANDLE_TOP_LEFT = 1
    HANDLE_TOP = 2
    HANDLE_TOP_RIGHT = 3
    HANDLE_LEFT = 4
    HANDLE_RIGHT = 5
    HANDLE_BOTTOM_LEFT = 6
    HANDLE_BOTTOM = 7
    HANDLE_BOTTOM_RIGHT = 8

    HANDLE_SIZE = +8.0
    HANDLE_SPACE = -4.0

    handleCursors = {
        HANDLE_TOP_LEFT: Qt.SizeFDiagCursor,
        HANDLE_TOP: Qt.SizeVerCursor,
        HANDLE_TOP_RIGHT: Qt.SizeBDiagCursor,
        HANDLE_LEFT: Qt.SizeHorCursor,
        HANDLE_RIGHT: Qt.SizeHorCursor,
        HANDLE_BOTTOM_LEFT: Qt.SizeBDiagCursor,
        HANDLE_BOTTOM: Qt.SizeVerCursor,
        HANDLE_BOTTOM_RIGHT: Qt.SizeFDiagCursor,
    }

    def __init__(self, *args, row_count=4, column_count=6):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}
        self.selected_handle = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.row_count, self.column_count = row_count, column_count
        self.on_moved = lambda: None
        self.update_handle_positions()

    def handle_at(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                # print(point, k)
                return k
        # print(point, None)
        return None

    def hoverMoveEvent(self, event):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        super().hoverMoveEvent(event)
        self.update_cursor(event)

    def update_cursor(self, event):
        cursor = Qt.ArrowCursor
        if self.isSelected():
            handle = self.handle_at(event.pos())
            if handle is not None:
                cursor = self.handleCursors[handle]
        self.setCursor(cursor)

    def hoverLeaveEvent(self, event):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        super().hoverLeaveEvent(event)
        self.update_cursor(event)

    def mousePressEvent(self, event):
        """
        Executed when the mouse is pressed on the item.
        """
        self.selected_handle = self.handle_at(event.pos())
        if self.selected_handle:
            self.mouse_press_pos = event.pos()
            self.mouse_press_rect = self.boundingRect()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.selected_handle is not None:
            self.interactive_resize(event.pos())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(event)
        self.selected_handle = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.HANDLE_SIZE + self.HANDLE_SPACE
        return self.rect().adjusted(-o, -o, o, o)

    def update_handle_positions(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.HANDLE_SIZE
        b = self.boundingRect()
        self.handles[self.HANDLE_TOP_LEFT] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.HANDLE_TOP] = QRectF(
            b.center().x() - s / 2, b.top(), s, s
        )
        self.handles[self.HANDLE_TOP_RIGHT] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.HANDLE_LEFT] = QRectF(
            b.left(), b.center().y() - s / 2, s, s
        )
        self.handles[self.HANDLE_RIGHT] = QRectF(
            b.right() - s, b.center().y() - s / 2, s, s
        )
        self.handles[self.HANDLE_BOTTOM_LEFT] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.HANDLE_BOTTOM] = QRectF(
            b.center().x() - s / 2, b.bottom() - s, s, s
        )
        self.handles[self.HANDLE_BOTTOM_RIGHT] = QRectF(
            b.right() - s, b.bottom() - s, s, s
        )

    def adjust_left(self, mouse_pos):
        rect = self.rect()
        rect.setLeft(
            self.mouse_press_rect.left() +
            mouse_pos.x() - self.mouse_press_pos.x() +
            self.HANDLE_SIZE + self.HANDLE_SPACE)
        self.setRect(rect)

    def adjust_right(self, mouse_pos):
        rect = self.rect()
        rect.setRight(
            self.mouse_press_rect.right() +
            mouse_pos.x() - self.mouse_press_pos.x() -
            self.HANDLE_SIZE - self.HANDLE_SPACE)
        self.setRect(rect)

    def adjust_top(self, mouse_pos):
        rect = self.rect()
        rect.setTop(
            self.mouse_press_rect.top() +
            mouse_pos.y() - self.mouse_press_pos.y() +
            self.HANDLE_SIZE + self.HANDLE_SPACE)
        self.setRect(rect)

    def adjust_bottom(self, mouse_pos):
        rect = self.rect()
        rect.setBottom(
            self.mouse_press_rect.bottom() +
            mouse_pos.y() - self.mouse_press_pos.y() -
            self.HANDLE_SIZE - self.HANDLE_SPACE)
        self.setRect(rect)

    def interactive_resize(self, mouse_pos):
        """
        Perform shape interactive resize.
        """
        self.prepareGeometryChange()

        if self.selected_handle == self.HANDLE_TOP_LEFT:
            self.adjust_top(mouse_pos)
            self.adjust_left(mouse_pos)
        elif self.selected_handle == self.HANDLE_TOP:
            self.adjust_top(mouse_pos)
        elif self.selected_handle == self.HANDLE_TOP_RIGHT:
            self.adjust_top(mouse_pos)
            self.adjust_right(mouse_pos)
        elif self.selected_handle == self.HANDLE_LEFT:
            self.adjust_left(mouse_pos)
        elif self.selected_handle == self.HANDLE_RIGHT:
            self.adjust_right(mouse_pos)
        elif self.selected_handle == self.HANDLE_BOTTOM_LEFT:
            self.adjust_left(mouse_pos)
            self.adjust_bottom(mouse_pos)
        elif self.selected_handle == self.HANDLE_BOTTOM:
            self.adjust_bottom(mouse_pos)
        elif self.selected_handle == self.HANDLE_BOTTOM_RIGHT:
            self.adjust_bottom(mouse_pos)
            self.adjust_right(mouse_pos)

        self.update_handle_positions()
        self.on_moved()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        painter.setPen(QPen(QColor(128, 128, 128), 1.0, Qt.SolidLine))
        for cell_rect in self.cell_rects():
            painter.drawRect(cell_rect)

        if self.isSelected():
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 255, 255, 255)))
            painter.setPen(
                QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            )
            for handle, rect in self.handles.items():
                if self.selected_handle is None or handle == self.selected_handle:
                    painter.drawEllipse(rect)

    def cell_rects(self):
        rect = self.rect()
        cell_width = rect.width() / self.column_count
        cell_height = rect.height() / self.row_count

        for row in range(self.row_count):
            y = rect.top() + rect.height() * row / self.row_count
            for column in range(self.column_count):
                x = rect.left() + rect.width() * column / self.column_count
                yield QRectF(x, y, cell_width, cell_height)
