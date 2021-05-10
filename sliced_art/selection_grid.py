from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem


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
        self.row_count, self.column_count = row_count, column_count

        # Callback method for when this is moved.
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
        self.mouse_press_pos = event.pos()
        self.mouse_press_rect = self.boundingRect()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """ Continue tracking movement while the mouse is pressed. """
        rect = self.drag_rect(event.pos())
        self.check_bounds(rect)
        self.setRect(rect)

        self.update_handle_positions()
        self.on_moved()

    def check_bounds(self, rect):
        # Figure out the limits of movement. I did it by updating the scene's
        # rect after the window resizes.
        scene_rect = self.scene().sceneRect()
        view_left = scene_rect.left()
        view_top = scene_rect.top()
        view_right = scene_rect.right()/2
        view_bottom = scene_rect.bottom()

        # Next, check if the rectangle has been dragged out of bounds.
        if rect.top() < view_top:
            if self.selected_handle is None:
                rect.translate(0, view_top - rect.top())
            else:
                rect.setTop(view_top)
        if rect.left() < view_left:
            if self.selected_handle is None:
                rect.translate(view_left - rect.left(), 0)
            else:
                rect.setLeft(view_left)
        if view_bottom < rect.bottom():
            if self.selected_handle is None:
                rect.translate(0, view_bottom - rect.bottom())
            else:
                rect.setBottom(view_bottom)
        if view_right < rect.right():
            if self.selected_handle is None:
                rect.translate(view_right - rect.right(), 0)
            else:
                rect.setRight(view_right)

        # Also check if the rectangle has been dragged inside out.
        if rect.width() < self.HANDLE_SIZE:
            if self.selected_handle in (self.HANDLE_TOP_LEFT,
                                        self.HANDLE_LEFT,
                                        self.HANDLE_BOTTOM_LEFT):
                rect.setLeft(rect.right() - self.HANDLE_SIZE)
            else:
                rect.setRight(rect.left() + self.HANDLE_SIZE)
        if rect.height() < self.HANDLE_SIZE:
            if self.selected_handle in (self.HANDLE_TOP_LEFT,
                                        self.HANDLE_TOP,
                                        self.HANDLE_TOP_RIGHT):
                rect.setTop(rect.bottom() - self.HANDLE_SIZE)
            else:
                rect.setBottom(rect.top() + self.HANDLE_SIZE)

    def drag_rect(self, pos):
        # Calculate how much the mouse has moved since the click.
        x_diff = pos.x() - self.mouse_press_pos.x()
        y_diff = pos.y() - self.mouse_press_pos.y()

        # Start with the rectangle as it was when clicked.
        rect = QRectF(self.mouse_press_rect)

        # Then adjust by the distance the mouse moved.
        if self.selected_handle is None:
            rect.translate(x_diff, y_diff)
        elif self.selected_handle == self.HANDLE_TOP_LEFT:
            rect.adjust(x_diff, y_diff, 0, 0)
        elif self.selected_handle == self.HANDLE_TOP:
            rect.setTop(rect.top() + y_diff)
        elif self.selected_handle == self.HANDLE_TOP_RIGHT:
            rect.setTop(rect.top() + y_diff)
            rect.setRight(rect.right() + x_diff)
        elif self.selected_handle == self.HANDLE_LEFT:
            rect.setLeft(rect.left() + x_diff)
        elif self.selected_handle == self.HANDLE_RIGHT:
            rect.setRight(rect.right() + x_diff)
        elif self.selected_handle == self.HANDLE_BOTTOM_LEFT:
            rect.setBottom(rect.bottom() + y_diff)
            rect.setLeft(rect.left() + x_diff)
        elif self.selected_handle == self.HANDLE_BOTTOM:
            rect.setBottom(rect.bottom() + y_diff)
        elif self.selected_handle == self.HANDLE_BOTTOM_RIGHT:
            rect.setBottom(rect.bottom() + y_diff)
            rect.setRight(rect.right() + x_diff)
        return rect

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
