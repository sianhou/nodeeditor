from PySide6.QtCore import QPointF
from PySide6.QtGui import QPen, QColor, QPainter, Qt, QPainterPath
from PySide6.QtWidgets import QGraphicsPathItem

from base.port import InputPort, OutputPort


class EdgeBase(QGraphicsPathItem):
    def __init__(self, source_port=InputPort, target_port=OutputPort, scene=None, parent=None):
        super(EdgeBase, self).__init__(parent=parent)

        self.setZValue(-1)

        self._source_port = source_port
        self._target_port = target_port
        self._scene = scene

        self._edge_color = self._source_port._port_color
        self._pen_default = QPen(QColor(self._edge_color))
        self._pen_default.setWidthF(2)

        self.addToScene()

    def paint(self, painter: QPainter, option, widget) -> None:
        self.updateEdgePath()

        painter.setPen(self._pen_default)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

        # if self.isSelected():
        #     self._shadow.setColor(self._shadow_color)
        #     self.setGraphicsEffect(self._shadow)
        # else:
        #     self._shadow.setColor('#00000000')
        #     self.setGraphicsEffect(self._shadow)

    def updateEdgePath(self):
        (s_x, s_y) = self._source_port.getPos()
        (t_x, t_y) = self._target_port.getPos()
        source_pos = QPointF(s_x, s_y)
        target_pos = QPointF(t_x, t_y)

        path = QPainterPath(source_pos)

        y_height = source_pos.y() - target_pos.y()
        y_height = y_height + 0.01 if y_height == 0 else y_height
        x_width = abs(target_pos.x() - source_pos.x())

        tagnent = float(x_width) / y_height * 0.5
        tagnent *= y_height

        if y_height > 0:
            if y_height > 150:
                y_height = 150
            tagnent += y_height

        # x_width = source_pos.x() - target_pos.x()
        # x_width = x_width + 0.01 if x_width == 0 else x_width
        # y_height = abs(target_pos.y() - source_pos.y())
        #
        # tagnent = float(y_height) / x_width * 0.5
        # tagnent *= x_width
        #
        # if x_width > 0:
        #     if x_width > 150:
        #         x_width = 150
        #     tagnent += x_width

        path.cubicTo(QPointF(source_pos.x(), source_pos.y() + tagnent),
                     QPointF(target_pos.x(), target_pos.y() - tagnent),
                     target_pos)

        self.setPath(path)

    def addToScene(self):
        self._scene.addItem(self)
        # 添加到相关的节点的port
        self._source_port.addEdge(self)
        self._target_port.addEdge(self)
        self._source_port.update()
        self._target_port.update()