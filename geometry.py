# ~*~ coding:utf-8 ~*~

import math
import numpy as np


class Geometry:
    def __init__(self):
        self.points = []  # Точки
        self.edges = []  # Рёбра
        self.faces = []  # Грани

        self.x_rotate_angle = 0
        self.y_rotate_angle = 0
        self.z_rotate_angle = 0

        # is_isometric
        self.angle_fi = 0
        self.angle_psi = 0

        # is_cabinet
        self.angle_alpha = 0
        self.L = 0

        # is_perspective
        self.angle_teta = 0
        self.angle_pfi = 0
        self.ro = 0
        self.d = 0

        self.dx = 0
        self.dy = 0
        self.dz = 0

        self.sx = 1
        self.sy = 1
        self.sz = 1

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
        self.m_perspective_w = np.zeros(0)

    def clear(self):
        self.points = []
        self.edges = []
        self.faces = []

    def apply_projection(self, name):
        # Конвертируем список точек в матрицу
        self.points = np.array(self.points)

        self.prepare_matrix()
        
        self.points = self.multiplication_matrix(self.points, self.mxr)
        self.points = self.multiplication_matrix(self.points, self.myr)
        self.points = self.multiplication_matrix(self.points, self.mzr)

        self.points = self.multiplication_matrix(self.points, self.mxyzm)
        self.points = self.multiplication_matrix(self.points, self.mxyzs)

        if name == "front":
            self.points = self.multiplication_matrix(self.points, self.m_frontal)
        elif name == "horizontal":
            self.points = self.multiplication_matrix(self.points, self.m_horizontal)
        elif name == "profile":
            self.points = self.multiplication_matrix(self.points, self.m_profile)
        elif name == "isometric":
            self.points = self.multiplication_matrix(self.points, self.m_isometric)
        elif name == "oblique":
            self.points = self.multiplication_matrix(self.points, self.m_cabinet)
        elif name == "perspective":
            # TODO Заставить перспективную проекцию работать
            move_x = 0
            move_y = 50
            move_z = 100
            for point in self.points:
                point[0] += move_x
                point[1] += move_y
                point[2] += move_z

            self.points = self.multiplication_matrix(self.points, self.m_perspective)
            self.points = self.multiplication_matrix(self.points, self.m_perspective_w)
            for point in self.points:
                if point[3] != 0:
                    point[0] /= point[3]
                    point[1] /= point[3]
                    point[2] /= point[3]
                    point[3] /= point[3]

            for point in self.points:
                point[0] += move_x
                point[1] += move_y
                point[2] += move_z

    def face_to_points(self, face):
        p1_index = face[0]
        x0 = self.points[p1_index][0]
        y0 = self.points[p1_index][1]
        z0 = self.points[p1_index][2]

        p2_index = face[1]
        x1 = self.points[p2_index][0]
        y1 = self.points[p2_index][1]
        z1 = self.points[p2_index][2]

        p3_index = face[2]
        x2 = self.points[p3_index][0]
        y2 = self.points[p3_index][1]
        z2 = self.points[p3_index][2]

        return x0, y0, z0, x1, y1, z1, x2, y2, z2

    @staticmethod
    def from_polar(radius, angle, z_axis):
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
        tmp = np.zeros(first.shape)
        for i in range(first.shape[0]):
            for l in range(second.shape[1]):
                tmp[i][l] = 0
                for j in range(second.shape[0]):
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

        if self.d == 0:
            self.d = 1
        self.m_perspective_w = np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0],
                                         [0, 0, 1, 1/self.d],
                                         [0, 0, 0, 0]])

        self.m_perspective = np.array([[-angle_teta_sin, -angle_pfi_cos * angle_teta_cos, -angle_pfi_sin * angle_teta_cos, 0],
                                       [angle_teta_cos, -angle_pfi_cos * angle_teta_sin, -angle_pfi_sin * angle_teta_sin, 0],
                                       [0, angle_pfi_sin, -angle_pfi_cos, 0],
                                       [0, 0, self.ro, 1]])