# ~*~ coding:utf-8 ~*~

import math
from PyQt5.QtCore import QRect, QSize, QPoint, Qt
from PyQt5.QtGui import QPainter, QPalette, QPen, QPolygon, QColor
from PyQt5.QtWidgets import QWidget, QColorDialog
from sphere import Sphere

# TODO Добавить источник света и сделать тени на объекте


class RenderArea(QWidget):
    def __init__(self, parent=None):
        super(RenderArea, self).__init__(parent)

        self.sphere = Sphere(self)

        self.pen = QPen(QColor(0, 0, 0), 0)
        self.faces_color = QColor(0, 255, 0)
        self.is_light = False

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

    def minimumSizeHint(self):
        return QSize(200, 200)

    def sizeHint(self):
        return QSize(400, 400)

    def set_pen_width(self, width):
        self.pen = QPen(self.pen.color(), width)
        self.update()

    def set_pen_color(self, label):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pen = QPen(color, self.pen.width())
            label_palette = QPalette()
            label_palette.setColor(QPalette.WindowText, color)
            label.setPalette(label_palette)
            label.setText("Цвет линии " + color.name())
        self.update()

    def set_faces_color(self, label):
        color = QColorDialog.getColor()
        if color.isValid():
            self.faces_color = color
            label_palette = QPalette()
            label_palette.setColor(QPalette.WindowText, color)
            label.setPalette(label_palette)
            label.setText("Цвет объекта" + color.name())
        self.update()

    def set_light(self, is_light):
        self.is_light = is_light
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)

        # Пересчитываем сферу
        self.sphere.recalculate()

        # Рисуем
        for face in self.sphere.geom.faces:
            self.draw_item(face, painter)

        # Окантовка виджета
        painter.setPen(self.palette().dark().color())
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))

    def draw_item(self, face, painter):
        if self.sphere.is_face_visible(face):
            polygon = QPolygon()
            for index, point_index in enumerate(face):
                p1_x = int(self.sphere.geom.points[face[index-1]][0])
                p1_y = int(self.sphere.geom.points[face[index-1]][1])
                p1_z = int(self.sphere.geom.points[face[index-1]][2])

                p2_x = int(self.sphere.geom.points[point_index][0])
                p2_y = int(self.sphere.geom.points[point_index][1])
                p2_z = int(self.sphere.geom.points[point_index][2])

                if self.sphere.projection_name == "front":
                    # Фронтальная проекция (вид спереди) -> z = 0
                    real_p1 = QPoint(p1_x, p1_y)
                    real_p2 = QPoint(p2_x, p2_y)
                elif self.sphere.projection_name == "horizontal":
                    # Горизонтальная проекция (вид сверху) -> y = 0
                    real_p1 = QPoint(p1_x, p1_z)
                    real_p2 = QPoint(p2_x, p2_z)
                elif self.sphere.projection_name == "profile":
                    # Профильная проекция (вид сбоку) -> x = 0
                    real_p1 = QPoint(p1_y, p1_z)
                    real_p2 = QPoint(p2_y, p2_z)
                else:
                    real_p1 = QPoint(p1_x, p1_y)
                    real_p2 = QPoint(p2_x, p2_y)

                # Точки для проволочного рисования
                real_p1.setX(self.width()/2 + real_p1.x())
                real_p1.setY(self.height()/2 - real_p1.y())
                real_p2.setX(self.width()/2 + real_p2.x())
                real_p2.setY(self.height()/2 - real_p2.y())

                # Полигоны для рисования с цветом
                polygon.append(real_p1)
                polygon.append(real_p2)

                if not self.is_light:
                    painter.drawLine(real_p1, real_p2)

            if self.is_light:
                painter.setBrush(self.sphere.get_face_light(face, self.faces_color))
                painter.drawPolygon(polygon)

    def set_projection(self, button):
        self.sphere.projection_name = button.objectName()
        self.update()
