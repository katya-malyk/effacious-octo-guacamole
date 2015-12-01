# ~*~ coding: utf-8 ~*~

import math
import numpy as np


class Sphere:
    def __init__(self, render_area):
        self.render_area = render_area

        self.approximation_step = 0
        self.radius = 0

        self.x_rotate_angle = 0
        self.y_rotate_angle = 0
        self.z_rotate_angle = 0

        self.dx = 0
        self.dy = 0
        self.dz = 0

        self.sx = 1
        self.sy = 1
        self.sz = 1

        self.is_frontal = False
        self.is_horizontal = False
        self.is_profile = False

        self.is_isometric = False
        self.angle_fi = 0
        self.angle_psi = 0

        self.is_cabinet = False
        self.angle_alpha = 0
        self.L = 0

        self.is_perspective = False
        self.angle_teta = 0
        self.angle_pfi = 0
        self.ro = 0
        self.d = 0

        self.points = []
        self.edges = []

        self.mxr = np.zeros(0)
        self.myr = np.zeros(0)
        self.mzr = np.zeros(0)
        self.mxyzm = np.zeros(0)
        self.mxyzs = np.zeros(0)
        self.m_horizontal = np.zeros(0)
        self.m_frontal = np.zeros(0)
        self.m_profile = np.zeros(0)
        self.m_isometric = np.zeros(0)
        self.m_cabinet = np.zeros(0)
        self.m_perspective = np.zeros(0)

    def recalculate(self):
        # Настройка шагов аппроксимации
        circle_count = self.approximation_step
        circle_points_count = self.approximation_step + 2

        # Считаем окружность
        self.points = []
        self.edges = []
        angle_step = 2*math.pi/circle_points_count
        for circle_number in range(1, circle_count+1):
            radius_for_point = self.radius * math.sqrt(1 - math.pow((circle_count - circle_number)/circle_count, 2))
            z_axis = self.radius * (circle_count-circle_number)/circle_count

            angle = 0
            while angle <= 2*math.pi:
                self.points.append(self.convert_from_polar(radius_for_point, angle, z_axis))
                self.points.append(self.convert_from_polar(radius_for_point, angle+angle_step, z_axis))
                self.edges.append((len(self.points)-2, len(self.points)-1))

                self.points.append(self.convert_from_polar(radius_for_point, angle, -z_axis))
                self.points.append(self.convert_from_polar(radius_for_point, angle+angle_step, -z_axis))
                self.edges.append((len(self.points)-2, len(self.points)-1))

                angle += angle_step

        for circle_number in range(0, circle_count):
            radius_for_point_1 = self.radius * math.sqrt(1 - math.pow((circle_count - circle_number-1)/circle_count, 2))
            radius_for_point_2 = self.radius * math.sqrt(1 - math.pow((circle_count - circle_number)/circle_count, 2))
            z_axis_for_point_1 = self.radius * (circle_count - circle_number - 1) / circle_count
            z_axis_for_point_2 = self.radius * (circle_count - circle_number) / circle_count

            angle = 0
            while angle <= 2*math.pi:
                self.points.append(self.convert_from_polar(radius_for_point_1, angle, z_axis_for_point_1))
                self.points.append(self.convert_from_polar(radius_for_point_2, angle, z_axis_for_point_2))
                self.edges.append((len(self.points)-2, len(self.points)-1))

                self.points.append(self.convert_from_polar(radius_for_point_1, angle, -z_axis_for_point_1))
                self.points.append(self.convert_from_polar(radius_for_point_2, angle, -z_axis_for_point_2))
                self.edges.append((len(self.points)-2, len(self.points)-1))

                angle += angle_step

        # Список списков превращается, превращается.. в массив
        self.points = np.array(self.points)

        self.prepare_matrix()

        self.points = self.multiplication_matrix(self.points, self.mxr)
        self.points = self.multiplication_matrix(self.points, self.myr)
        self.points = self.multiplication_matrix(self.points, self.mzr)

        self.points = self.multiplication_matrix(self.points, self.mxyzm)
        self.points = self.multiplication_matrix(self.points, self.mxyzs)

        if self.is_frontal:
            self.points = self.multiplication_matrix(self.points, self.m_frontal)
        elif self.is_horizontal:
            self.points = self.multiplication_matrix(self.points, self.m_horizontal)
        elif self.is_profile:
            self.points = self.multiplication_matrix(self.points, self.m_profile)
        elif self.is_isometric:
            self.points = self.multiplication_matrix(self.points, self.m_isometric)
        elif self.is_cabinet:
            self.points = self.multiplication_matrix(self.points, self.m_cabinet)
        elif self.is_perspective:
            temp = self.multiplication_matrix(self.points, self.m_perspective)
            for i in range(len(temp)):
                if temp[i][2] != 0:
                    self.points[i][0] = temp[i][0] * self.d / temp[i][2]
                    self.points[i][1] = temp[i][1] * self.d / temp[i][2]
                    self.points[i][2] = self.d

    def set_approximation_step(self, step):
        self.approximation_step = step
        self.render_area.update()

    def set_radius(self, radius):
        self.radius = radius * 6
        self.render_area.update()

    def set_x_rotate_angle(self, angle):
        self.x_rotate_angle = angle
        self.render_area.update()

    def set_y_rotate_angle(self, angle):
        self.y_rotate_angle = angle
        self.render_area.update()

    def set_z_rotate_angle(self, angle):
        self.z_rotate_angle = angle
        self.render_area.update()

    def set_dx(self, value):
        self.dx = value
        self.render_area.update()

    def set_dy(self, value):
        self.dy = value
        self.render_area.update()

    def set_dz(self, value):
        self.dz = value
        self.render_area.update()

    def set_sx(self, value):
        self.sx = value
        self.render_area.update()

    def set_sy(self, value):
        self.sy = value
        self.render_area.update()

    def set_sz(self, value):
        self.sz = value
        self.render_area.update()

    def set_frontal(self):
        self.is_cabinet = False
        self.is_frontal = not self.is_frontal
        self.is_horizontal = False
        self.is_profile = False
        self.is_isometric = False
        self.is_perspective = False
        self.render_area.update()

    def set_horizontal(self):
        self.is_cabinet = False
        self.is_frontal = False
        self.is_horizontal = not self.is_horizontal
        self.is_profile = False
        self.is_isometric = False
        self.is_perspective = False
        self.render_area.update()

    def set_profile(self):
        self.is_cabinet = False
        self.is_frontal = False
        self.is_horizontal = False
        self.is_profile = not self.is_profile
        self.is_isometric = False
        self.is_perspective = False
        self.render_area.update()

    def set_isometric(self):
        self.is_cabinet = False
        self.is_frontal = False
        self.is_horizontal = False
        self.is_profile = False
        self.is_isometric = not self.is_isometric
        self.is_perspective = False
        self.render_area.update()

    def set_cabinet(self):
        self.is_frontal = False
        self.is_horizontal = False
        self.is_profile = False
        self.is_isometric = False
        self.is_cabinet = not self.is_cabinet
        self.is_perspective = False
        self.render_area.update()

    def set_perspective(self):
        self.is_frontal = False
        self.is_horizontal = False
        self.is_profile = False
        self.is_isometric = False
        self.is_cabinet = False
        self.is_perspective = not self.is_perspective
        self.render_area.update()

    def set_angle_fi(self, value):
        self.angle_fi = value
        self.render_area.update()

    def set_angle_psi(self, value):
        self.angle_psi = value
        self.render_area.update()

    def set_angle_alpha(self, value):
        self.angle_alpha = value
        self.render_area.update()

    def set_L(self, value):
        self.L = value
        self.render_area.update()

    def set_angle_pfi(self, value):
        self.angle_pfi = value
        self.render_area.update()

    def set_angle_teta(self, value):
        self.angle_teta = value
        self.render_area.update()

    def set_ro(self, value):
        self.ro = value
        self.render_area.update()

    def set_d(self, value):
        self.d = value
        self.render_area.update()

    @staticmethod
    def convert_from_polar(radius, angle, z_axis):
        """
        Конвертирует координату из двумерной полярной системы координат в декартову трёхмерную
        :param radius: Радиус до точке в полярной системе координат
        :param angle: Угол до точки в полярной системе координат
        :param z_axis: Ось z, передаётся напрямую
        :return: Список координат точки
        """
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = z_axis
        return x, y, z, 1

    @staticmethod
    def multiplication_matrix(first, second):
        """
        Умножение матриц, аналог функции np.dot(a,b)
        :param first: Левая матрица
        :param second: Правая матрица
        :return: Произведение матриц
        """
        tmp = np.zeros(first.shape, dtype=int)
        for i in range(len(first)):
            for l in range(len(second)):
                tmp[i][l] = 0
                for j in range(len(second)):
                    tmp[i][l] += first[i][j] * second[j][l]
        return tmp

    def prepare_matrix(self):
        """
        Подготавливает матрицы различных преобразований
        """
        # Матрицы поворота по осям
        x_rotate_cos = math.cos(self.x_rotate_angle * math.pi / 180)
        x_rotate_sin = math.sin(self.x_rotate_angle * math.pi / 180)
        self.mxr = np.array([[1, 0,             0,            0],
                             [0, x_rotate_cos,  x_rotate_sin, 0],
                             [0, -x_rotate_sin, x_rotate_cos, 0],
                             [0, 0,             0,            1]])

        y_rotate_cos = math.cos(self.y_rotate_angle * math.pi / 180)
        y_rotate_sin = math.sin(self.y_rotate_angle * math.pi / 180)
        self.myr = np.array([[y_rotate_cos, 0, -y_rotate_sin, 0],
                        [0,            1, 0,             0],
                        [y_rotate_sin, 0, y_rotate_cos,  0],
                        [0,            0, 0,             1]])

        z_rotate_cos = math.cos(self.z_rotate_angle * math.pi / 180)
        z_rotate_sin = math.sin(self.z_rotate_angle * math.pi / 180)
        self.mzr = np.array([[z_rotate_cos,  z_rotate_sin, 0, 0],
                        [-z_rotate_sin, z_rotate_cos, 0, 0],
                        [0,             0,            1, 0],
                        [0,             0,            0, 1]])

        # Матрицы перемещения
        self.mxyzm = np.array([[1,       0,       0,       0],
                          [0,       1,       0,       0],
                          [0,       0,       1,       0],
                          [self.dx, self.dy, self.dz, 1]])

        # Матрица масштабирования
        self.mxyzs = np.array([[self.sx, 0,       0,       0],
                          [0,       self.sy, 0,       0],
                          [0,       0,       self.sz, 0],
                          [0,       0,       0,       1]])

        # Матрицы ортографических проекций
        self.m_horizontal = np.array([[1, 0, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])

        self.m_frontal = np.array([[1, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 0, 0, 0],
                              [0, 0, 0, 1]])

        self.m_profile = np.array([[0, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

        # Матрица изометрической проекции
        angle_fi_sin = math.sin(self.angle_fi * math.pi / 180)
        angle_psi_sin = math.sin(self.angle_psi * math.pi / 180)
        angle_fi_cos = math.cos(self.angle_fi * math.pi / 180)
        angle_psi_cos = math.cos(self.angle_psi * math.pi / 180)
        self.m_isometric = np.array([[angle_psi_cos, angle_fi_sin*angle_psi_sin, 0, 0],
                                [0, angle_fi_cos, 0, 0],
                                [angle_psi_sin, -angle_fi_sin*angle_psi_cos, 0, 0],
                                [0, 0, 0, 1]])

        # Матрица косоугольной проекции
        angle_alpha_sin = math.sin(self.angle_alpha * math.pi / 180)
        angle_alpha_cos = math.cos(self.angle_alpha * math.pi / 180)
        self.m_cabinet = np.array([[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [self.L*angle_alpha_cos, self.L*angle_alpha_sin, 0, 0],
                                [0, 0, 0, 1]])

        # Матрицы перспективной проекции
        angle_teta_sin = math.sin(self.angle_teta*math.pi / 180)
        angle_teta_cos = math.cos(self.angle_teta*math.pi / 180)

        angle_pfi_sin = math.sin(self.angle_pfi*math.pi / 180)
        angle_pfi_cos = math.cos(self.angle_pfi*math.pi / 180)

        self.m_perspective = np.array([[angle_teta_cos, -(angle_pfi_cos*angle_teta_sin), -(angle_pfi_sin*angle_teta_sin), 0],
                                  [angle_teta_sin, angle_pfi_cos*angle_teta_cos, angle_pfi_sin*angle_teta_cos, 0],
                                  [0, angle_pfi_sin, -angle_pfi_cos, 0],
                                  [0, 0, self.ro, 1]])
