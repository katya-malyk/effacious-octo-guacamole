# ~*~ coding: utf-8 ~*~

import math
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import (QPainter, QPalette, QPen)
from PyQt5.QtWidgets import QWidget
from sphere import Sphere


class RenderArea(QWidget):
    def __init__(self, parent=None):
        super(RenderArea, self).__init__(parent)

        self.sphere = Sphere(self)

        self.pen = QPen()

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

    def minimumSizeHint(self):
        return QSize(200, 200)

    def sizeHint(self):
        return QSize(400, 400)

    def set_pen_width(self, width):
        self.pen = QPen(Qt.red, width)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)

        self.sphere.recalculate()

        # Рисуем
        for edge in self.sphere.edges:
            first_point_index = edge[0]
            first_point_x = self.sphere.points[first_point_index][0]
            first_point_y = self.sphere.points[first_point_index][1]
            first_point_z = self.sphere.points[first_point_index][2]

            second_point_index = edge[1]
            second_point_x = self.sphere.points[second_point_index][0]
            second_point_y = self.sphere.points[second_point_index][1]
            second_point_z = self.sphere.points[second_point_index][2]

            if self.sphere.is_frontal:
                # Фронтальная проекция (вид спереди) -> z = 0
                self.draw_line(self.width()/2 + first_point_x,
                               self.height()/2 + first_point_y,
                               self.width()/2 + second_point_x,
                               self.height()/2 + second_point_y,
                               painter)
            elif self.sphere.is_horizontal:
                # Горизонтальная проекция (вид сверху) -> y = 0
                self.draw_line(self.width()/2 + first_point_x,
                               self.height()/2 + first_point_z,
                               self.width()/2 + second_point_x,
                               self.height()/2 + second_point_z,
                               painter)
            elif self.sphere.is_profile:
                # Профильная проекция (вид сбоку) -> x = 0
                self.draw_line(self.width()/2 + first_point_y,
                               self.height()/2 + first_point_z,
                               self.width()/2 + second_point_y,
                               self.height()/2 + second_point_z,
                               painter)

            else:
                self.draw_line(self.width()/2 + first_point_x,
                               self.height()/2 + first_point_y,
                               self.width()/2 + second_point_x,
                               self.height()/2 + second_point_y,
                               painter)

        # Окантовка виджета
        painter.setPen(self.palette().dark().color())
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))

    @staticmethod
    def draw_line(x0, y0, x1, y1, painter):
        step = False
        # if the line is steep, we transpose the image
        if math.fabs(x0-x1) < math.fabs(y0-y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            step = True

        # make it left-to-right
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        x = x0
        while x <= x1:
            t = (x - x0)/(x1 - x0)
            y = y0*(1.-t) + y1*t
            if math.isnan(y):
                y = 0

            if step:
                # if transposed, de-transpose
                painter.drawPoint(int(y), int(x))
            else:
                painter.drawPoint(int(x), int(y))
            x += 1
