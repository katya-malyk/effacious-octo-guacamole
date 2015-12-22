# ~*~ coding:utf-8 ~*~

import math
import numpy as np


class Geometry:
    """
    Класс для математики - хранение точек, матриц, совершение преобразований
    """
    def __init__(self):
        self.clear_points = []
        self.points = []  # Точки
        self.edges = []  # Рёбра
        self.faces = []  # Грани

        # Углы поворота
        self.x_rotate_angle = 0
        self.y_rotate_angle = 0
        self.z_rotate_angle = 0

        # Координаты перемещения
        self.x_move = 0
        self.y_move = 0
        self.z_move = 0

        # Коэффициенты масштабирования
        self.x_scale = 1
        self.y_scale = 1
        self.z_scale = 1

        # Углы аксонометрической проекции
        self.axonometric_angle_fi = 0
        self.axonometric_angle_psi = 0

        # Параметры косоугольной проекции
        self.oblique_angle_alpha = 0
        self.oblique_L = 0

        # Параметры перспективной проекции
        self.perspective_angle_teta = 0
        self.perspective_angle_fi = 0
        self.perspective_ro = 0
        self.perspective_d = 0

        self.m_rotate_x = np.zeros(0)
        self.m_rotate_y = np.zeros(0)
        self.m_rotate_z = np.zeros(0)
        self.m_move = np.zeros(0)
        self.m_scale = np.zeros(0)
        self.m_horizontal = np.zeros(0)
        self.m_frontal = np.zeros(0)
        self.m_profile = np.zeros(0)
        self.m_axonometric = np.zeros(0)
        self.m_oblique = np.zeros(0)
        self.m_perspective = np.zeros(0)
        self.m_perspective_w = np.zeros(0)

    def clear(self):
        self.clear_points = []
        self.points = []
        self.edges = []
        self.faces = []

    def apply_projection(self, name):
        # Конвертируем список точек в матрицу
        self.clear_points = np.array(self.points)
        self.points = np.array(self.points)

        self.prepare_matrix()

        if name == "default":
            # Поворот, перемещение и масштаб только для проекции по умолчанию
            self.points = self.multiplication_matrix(self.points, self.m_rotate_x)
            self.points = self.multiplication_matrix(self.points, self.m_rotate_y)
            self.points = self.multiplication_matrix(self.points, self.m_rotate_z)

            self.points = self.multiplication_matrix(self.points, self.m_move)
            self.points = self.multiplication_matrix(self.points, self.m_scale)

            self.points = self.multiplication_matrix(self.points, self.m_frontal)
        if name == "front":
            self.points = self.multiplication_matrix(self.points, self.m_frontal)
        elif name == "horizontal":
            self.points = self.multiplication_matrix(self.points, self.m_horizontal)
        elif name == "profile":
            self.points = self.multiplication_matrix(self.points, self.m_profile)
        elif name == "axonometric":
            self.points = self.multiplication_matrix(self.points, self.m_axonometric)
        elif name == "oblique":
            self.points = self.multiplication_matrix(self.points, self.m_oblique)
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
        self.m_rotate_x = np.array([[1, 0, 0, 0],
                                    [0, x_rotate_cos,  x_rotate_sin, 0],
                                    [0, -x_rotate_sin, x_rotate_cos, 0],
                                    [0, 0,             0,            1]])

        y_rotate_cos = math.cos(self.y_rotate_angle * math.pi / 180)
        y_rotate_sin = math.sin(self.y_rotate_angle * math.pi / 180)
        self.m_rotate_y = np.array([[y_rotate_cos, 0, -y_rotate_sin, 0],
                                    [0,            1, 0,             0],
                                    [y_rotate_sin, 0, y_rotate_cos,  0],
                                    [0,            0, 0,             1]])

        z_rotate_cos = math.cos(self.z_rotate_angle * math.pi / 180)
        z_rotate_sin = math.sin(self.z_rotate_angle * math.pi / 180)
        self.m_rotate_z = np.array([[z_rotate_cos, z_rotate_sin, 0, 0],
                                    [-z_rotate_sin, z_rotate_cos, 0, 0],
                                    [0,             0,            1, 0],
                                    [0,             0,            0, 1]])

        # Матрицы перемещения
        self.m_move = np.array([[1, 0, 0, 0],
                                [0,           1,           0,           0],
                                [0,           0,           1,           0],
                                [self.x_move, self.y_move, self.z_move, 1]])

        # Матрица масштабирования
        self.m_scale = np.array([[self.x_scale, 0, 0, 0],
                                 [0,            self.y_scale, 0,            0],
                                 [0,            0,            self.z_scale, 0],
                                 [0,            0,            0,            1]])

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

        # Матрица аксонометрической проекции
        angle_fi_sin = math.sin(self.axonometric_angle_fi * math.pi / 180)
        angle_psi_sin = math.sin(self.axonometric_angle_psi * math.pi / 180)
        angle_fi_cos = math.cos(self.axonometric_angle_fi * math.pi / 180)
        angle_psi_cos = math.cos(self.axonometric_angle_psi * math.pi / 180)
        self.m_axonometric = np.array([[angle_psi_cos, angle_fi_sin * angle_psi_sin, 0, 0],
                                       [0,             angle_fi_cos,                0, 0],
                                       [angle_psi_sin, -angle_fi_sin*angle_psi_cos, 0, 0],
                                       [0,             0,                           0, 1]])

        # Матрица косоугольной проекции
        angle_alpha_sin = math.sin(self.oblique_angle_alpha * math.pi / 180)
        angle_alpha_cos = math.cos(self.oblique_angle_alpha * math.pi / 180)
        self.m_oblique = np.array([[1,                                0,                                0, 0],
                                   [0,                                1,                                0, 0],
                                   [self.oblique_L * angle_alpha_cos, self.oblique_L * angle_alpha_sin, 0, 0],
                                   [0,                                0,                                0, 1]])

        # Матрицы перспективной проекции
        angle_teta_sin = math.sin(self.perspective_angle_teta*math.pi / 180)
        angle_teta_cos = math.cos(self.perspective_angle_teta*math.pi / 180)

        angle_fi_sin = math.sin(self.perspective_angle_fi*math.pi / 180)
        angle_fi_cos = math.cos(self.perspective_angle_fi*math.pi / 180)

        if self.perspective_d == 0:
            self.perspective_d = 1
        self.m_perspective_w = np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0],
                                         [0, 0, 1, 1/self.perspective_d],
                                         [0, 0, 0, 0]])

        self.m_perspective = np.array([[-angle_teta_sin, -angle_fi_cos * angle_teta_cos, -angle_fi_sin * angle_teta_cos, 0],
                                       [angle_teta_cos,  -angle_fi_cos * angle_teta_sin, -angle_fi_sin * angle_teta_sin, 0],
                                       [0,               angle_fi_sin,                   -angle_fi_cos,                  0],
                                       [0,               0,                              self.perspective_ro,            1]])
