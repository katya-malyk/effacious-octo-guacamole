# ~*~ coding:utf-8 ~*~

from PyQt5.Qt import QColor
import math
import numpy as np
from geometry import Geometry


class Sphere:
    """
    Класс для общего описания сферы
    """
    def __init__(self, render_area):
        self.render_area = render_area

        self.approximation_step = 0
        self.radius = 0

        self.projection_name = "default"

        # Координаты источника света
        self.light_x = 0
        self.light_y = 0
        self.light_z = -1000

        self.geom = Geometry()

    def recalculate(self):
        # Настройка шагов аппроксимации
        circle_count = self.approximation_step
        circle_points_count = self.approximation_step + 2

        # Считаем окружность
        self.geom.clear()
        angle_step = 2*math.pi/circle_points_count
        for circle_number in range(0, circle_count):
            radius_for_point_1 = self.radius * math.sqrt(1 - math.pow((circle_count - (circle_number+1))/circle_count, 2))
            z_axis_for_point_1 = self.radius * (circle_count-(circle_number+1))/circle_count

            radius_for_point_2 = self.radius * math.sqrt(1 - math.pow((circle_count - circle_number)/circle_count, 2))
            z_axis_for_point_2 = self.radius * (circle_count - circle_number) / circle_count

            angle = 0
            while angle < 2*math.pi:
                self.geom.points.append(Geometry.from_polar(radius_for_point_1, angle, z_axis_for_point_1))
                self.geom.points.append(Geometry.from_polar(radius_for_point_1, angle+angle_step, z_axis_for_point_1))
                self.geom.edges.append((len(self.geom.points)-2, len(self.geom.points)-1))

                self.geom.points.append(Geometry.from_polar(radius_for_point_2, angle, z_axis_for_point_2))
                self.geom.points.append(Geometry.from_polar(radius_for_point_2, angle+angle_step, z_axis_for_point_2))
                self.geom.edges.append((len(self.geom.points)-2, len(self.geom.points)-1))

                angle += angle_step

            angle = 2*math.pi
            while angle > 0:
                self.geom.points.append(Geometry.from_polar(radius_for_point_1, angle, -z_axis_for_point_1))
                self.geom.points.append(Geometry.from_polar(radius_for_point_1, angle-angle_step, -z_axis_for_point_1))
                self.geom.edges.append((len(self.geom.points)-2, len(self.geom.points)-1))

                self.geom.points.append(Geometry.from_polar(radius_for_point_2, angle, -z_axis_for_point_2))
                self.geom.points.append(Geometry.from_polar(radius_for_point_2, angle-angle_step, -z_axis_for_point_2))
                self.geom.edges.append((len(self.geom.points)-2, len(self.geom.points)-1))

                angle -= angle_step

        for index in range(0, len(self.geom.points), 4):
            self.geom.faces.append((index, index+1, index+3, index+2))

        self.geom.apply_projection(self.projection_name)

    def is_face_visible(self, face):
        """
        Определение видимости грани на основе алгоритма Робертса
        :param face: грань
        :return: True, если видимо, иначе False
        """
        p1_index = face[0]
        x0 = self.geom.points[p1_index][0]
        y0 = self.geom.points[p1_index][1]
        z0 = self.geom.points[p1_index][2]

        p2_index = face[1]
        x1 = self.geom.points[p2_index][0]
        y1 = self.geom.points[p2_index][1]
        z1 = self.geom.points[p2_index][2]

        p3_index = face[2]
        x2 = self.geom.points[p3_index][0]
        y2 = self.geom.points[p3_index][1]
        z2 = self.geom.points[p3_index][2]

        a = y0*(z1 - z2) + y1*(z2 - z0) + y2*(z0 - z1)
        b = z0*(x1 - x2) + z1*(x2 - x0) + z2*(x0 - x1)
        c = x0*(y1 - y2) + x1*(y2 - y0) + x2*(y0 - y1)
        d = -(x0*(y1*z2 - y2*z1) + x1*(y2*z0 - y0*z2) + x2*(y0*z1 - y1*z0))

        """
        Знак result = Ax + By + Cz + D определяет, с какой стороны по отношению к плоскости находится точка s(x,y,z,w).
        Если result > 0, то точка внутри тела
        Если result < 0 - на противаположной стороне, а в случае result = 0 точка принадлежит плоскости.
        """

        s = np.array([[1, 1, -1000, 1]])
        p = np.array([[a],
                      [b],
                      [c],
                      [d]])
        result = Geometry.multiplication_matrix(s, p)

        return True if result[0][0] < 0 else False

    def get_face_light(self, face, color):
        """
        Закраска грани с учётом освещения на основе вычисления угла между нормалью грани и вектором освещения
        :param face: грань
        :param color: цвет грани
        :return: цвет
        """
        p1_index = face[0]
        x0 = self.geom.clear_points[p1_index][0]
        y0 = self.geom.clear_points[p1_index][1]
        z0 = self.geom.clear_points[p1_index][2]

        p2_index = face[1]
        x1 = self.geom.clear_points[p2_index][0]
        y1 = self.geom.clear_points[p2_index][1]
        z1 = self.geom.clear_points[p2_index][2]

        p3_index = face[2]
        x2 = self.geom.clear_points[p3_index][0]
        y2 = self.geom.clear_points[p3_index][1]
        z2 = self.geom.clear_points[p3_index][2]

        # Вычисляем два вектора, принадлежащих грани
        a_x = x1 - x0
        a_y = y1 - y0
        a_z = z1 - z0

        b_x = x2 - x1
        b_y = y2 - y1
        b_z = z2 - z1

        # Считаем нормаль к грани по найденным векторам
        normal_x = a_y * b_z - a_z * b_y
        normal_y = a_x * b_z - a_z * b_x
        normal_z = a_x * b_y - a_y * b_x

        # Длина нормали
        normal_length = math.sqrt(math.pow(normal_x, 2) + math.pow(normal_y, 2) + math.pow(normal_z, 2))

        # Зная координаты источника света, можно вычислить длину вектора от источника света до точки рассмотрения:
        light_length = math.sqrt(math.pow(self.light_x, 2) + math.pow(self.light_y, 2) + math.pow(self.light_z, 2))

        normal_length = normal_length if normal_length != 0 else 0.0001
        light_length = light_length if light_length != 0 else 0.0001

        # Косинус угла между данными векторами находим следующим образом:
        result = (normal_x * self.light_x + normal_y * self.light_y + normal_z * self.light_z)/(normal_length * light_length)

        # Находим интенсивность
        return QColor(int(color.red() * (0.5 + 0.5 * result)),
                      int(color.green() * (0.5 + 0.5 * result)),
                      int(color.blue() * (0.5 + 0.5 * result)))

    def set_approximation_step(self, step):
        self.approximation_step = step
        self.render_area.update()

    def set_radius(self, radius):
        self.radius = radius * 6
        self.render_area.update()

    def set_x_rotate_angle(self, angle):
        self.geom.x_rotate_angle = angle
        self.render_area.update()

    def set_y_rotate_angle(self, angle):
        self.geom.y_rotate_angle = angle
        self.render_area.update()

    def set_z_rotate_angle(self, angle):
        self.geom.z_rotate_angle = angle
        self.render_area.update()

    def set_x_move(self, value):
        self.geom.x_move = value
        self.render_area.update()

    def set_y_move(self, value):
        self.geom.y_move = value
        self.render_area.update()

    def set_z_move(self, value):
        self.geom.z_move = value
        self.render_area.update()

    def set_x_scale(self, value):
        self.geom.x_scale = value
        self.render_area.update()

    def set_y_scale(self, value):
        self.geom.y_scale = value
        self.render_area.update()

    def set_z_scale(self, value):
        self.geom.z_scale = value
        self.render_area.update()

    def set_axonometric_angle_fi(self, value):
        self.geom.axonometric_angle_fi = value
        self.render_area.update()

    def set_axonometric_angle_psi(self, value):
        self.geom.axonometric_angle_psi = value
        self.render_area.update()

    def set_oblique_angle_alpha(self, value):
        self.geom.oblique_angle_alpha = value
        self.render_area.update()

    def set_oblique_L(self, value):
        self.geom.oblique_L = value
        self.render_area.update()

    def set_perspective_angle_fi(self, value):
        self.geom.perspective_angle_fi = value
        self.render_area.update()

    def set_perspective_angle_teta(self, value):
        self.geom.perspective_angle_teta = value
        self.render_area.update()

    def set_perspective_ro(self, value):
        self.geom.perspective_ro = value
        self.render_area.update()

    def set_perspective_d(self, value):
        self.geom.perspective_d = value
        self.render_area.update()

    def set_light_x(self, x):
        self.light_x = x*10
        self.render_area.update()

    def set_light_y(self, y):
        self.light_y = -y*10
        self.render_area.update()

    def set_light_z(self, z):
        self.light_z = -z*10
        self.render_area.update()
