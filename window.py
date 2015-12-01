# ~*~ coding: utf-8 ~*~

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QSlider, QLabel,
                             QSpinBox, QWidget, QPushButton)
from render_area import RenderArea

# TODO x,y,z центра заставить работать
# TODO радиус сделать не дробным
# TODO Сместить настройки в левый бок
# TODO Добавить QLabel подписи к настройкам
# TODO Прокомментировать код и убрать лишнее


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.render_area = RenderArea()

        pen_width_SpinBox = self.create_spinbox(3, 0, 20)
        approximation_step_SpinBox = self.create_spinbox(1, 1, 50)
        radius_SpinBox = self.create_spinbox(30, 1, 50)

        pen_width_Label = QLabel("Ширина линии:")
        pen_width_Label.setBuddy(pen_width_SpinBox)
        approximation_step_Label = QLabel("Шаг аппроксимации:")
        approximation_step_Label.setBuddy(approximation_step_SpinBox)
        radius_Label = QLabel("Радиус сферы:")
        radius_Label.setBuddy(radius_SpinBox)

        x_rotate_Label = QLabel("Поворот по оси x")
        y_rotate_Label = QLabel("Поворот по оси y")
        z_rotate_Label = QLabel("Поворот по оси z")

        x_rotate_Slider = self.create_slider(0, 0, 360, 1, 60, 1)
        y_rotate_Slider = self.create_slider(0, 0, 360, 1, 60, 1)
        z_rotate_Slider = self.create_slider(0, 0, 360, 1, 60, 1)

        #Move
        x_move_Label = QLabel("Перемещение по оси x")
        y_move_Label = QLabel("Перемещение по оси y")
        z_move_Label = QLabel("Перемещение по оси z")

        x_move_Slider = self.create_slider(0, -300, 300, 1, 60, 1)
        y_move_Slider = self.create_slider(0, -300, 300, 1, 60, 1)
        z_move_Slider = self.create_slider(0, -300, 300, 1, 60, 1)

        #Scale

        x_scale_Label = QLabel("Масштабирование по оси x")
        y_scale_Label = QLabel("Масштабирование по оси y")
        z_scale_Label = QLabel("Масштабирование по оси z")

        x_scale_Slider = self.create_slider(1, 1, 10, 1, 60, 1)
        y_scale_Slider = self.create_slider(1, 1, 10, 1, 60, 1)
        z_scale_Slider = self.create_slider(1, 1, 10, 1, 60, 1)

        frontal_Button = QPushButton(self)
        frontal_Button.setText('Фронтальная')
        horizontal_Button = QPushButton(self)
        horizontal_Button.setText('Горизонтальная')
        profile_Button = QPushButton(self)
        profile_Button.setText('Профильная')

        isometric_Button = QPushButton(self)
        isometric_Button.setText('Изометрическая')

        fi_angle_Label = QLabel("Угол фи:")
        fi_angle_SpinBox = self.create_spinbox(0, 0, 360)
        fi_angle_Label.setBuddy(fi_angle_SpinBox)

        psi_angle_Label = QLabel("Угол пси:")
        psi_angle_SpinBox = self.create_spinbox(0, 0, 360)
        psi_angle_Label.setBuddy(psi_angle_SpinBox)

        cabinet_Button = QPushButton(self)
        cabinet_Button.setText('Косоугольная')

        alpha_angle_Label = QLabel("Угол альфа:")
        alpha_angle_SpinBox = self.create_spinbox(0, 0, 360)
        alpha_angle_Label.setBuddy(alpha_angle_SpinBox)

        L_Label = QLabel("L:")
        L_SpinBox = self.create_spinbox(0, 1, 100)
        L_Label.setBuddy(L_SpinBox)

        perspective_Button = QPushButton(self)
        perspective_Button.setText('Перспективная')

        teta_angle_Label = QLabel("Угол тета:")
        teta_angle_SpinBox = self.create_spinbox(0, 0, 360)
        teta_angle_Label.setBuddy(teta_angle_SpinBox)

        pfi_angle_Label = QLabel("Угол фи:")
        pfi_angle_SpinBox = self.create_spinbox(0, 0, 360)
        teta_angle_Label.setBuddy(pfi_angle_SpinBox)

        d_Label = QLabel("d:")
        d_SpinBox = self.create_spinbox(0, 0, 100)
        d_Label.setBuddy(d_SpinBox)

        ro_Label = QLabel("Ро:")
        ro_SpinBox = self.create_spinbox(0, 0, 100)
        ro_Label.setBuddy(ro_SpinBox)

        pen_width_SpinBox.valueChanged.connect(self.render_area.set_pen_width)
        approximation_step_SpinBox.valueChanged.connect(self.render_area.sphere.set_approximation_step)
        radius_SpinBox.valueChanged.connect(self.render_area.sphere.set_radius)
        x_rotate_Slider.valueChanged.connect(self.render_area.sphere.set_x_rotate_angle)
        y_rotate_Slider.valueChanged.connect(self.render_area.sphere.set_y_rotate_angle)
        z_rotate_Slider.valueChanged.connect(self.render_area.sphere.set_z_rotate_angle)

        x_move_Slider.valueChanged.connect(self.render_area.sphere.set_dx)
        y_move_Slider.valueChanged.connect(self.render_area.sphere.set_dy)
        z_move_Slider.valueChanged.connect(self.render_area.sphere.set_dz)

        x_scale_Slider.valueChanged.connect(self.render_area.sphere.set_sx)
        y_scale_Slider.valueChanged.connect(self.render_area.sphere.set_sy)
        z_scale_Slider.valueChanged.connect(self.render_area.sphere.set_sz)

        frontal_Button.clicked.connect(self.render_area.sphere.set_frontal)
        horizontal_Button.clicked.connect(self.render_area.sphere.set_horizontal)
        profile_Button.clicked.connect(self.render_area.sphere.set_profile)

        isometric_Button.clicked.connect(self.render_area.sphere.set_isometric)
        fi_angle_SpinBox.valueChanged.connect(self.render_area.sphere.set_angle_fi)
        psi_angle_SpinBox.valueChanged.connect(self.render_area.sphere.set_angle_psi)

        cabinet_Button.clicked.connect(self.render_area.sphere.set_cabinet)
        alpha_angle_SpinBox.valueChanged.connect(self.render_area.sphere.set_angle_alpha)
        L_SpinBox.valueChanged.connect(self.render_area.sphere.set_L)

        perspective_Button.clicked.connect(self.render_area.sphere.set_perspective)
        teta_angle_SpinBox.valueChanged.connect(self.render_area.sphere.set_angle_teta)
        pfi_angle_SpinBox.valueChanged.connect(self.render_area.sphere.set_angle_pfi)
        d_SpinBox.valueChanged.connect(self.render_area.sphere.set_d)
        ro_SpinBox.valueChanged.connect(self.render_area.sphere.set_ro)

        main_layout = QGridLayout()
        main_layout.addWidget(self.render_area, 0, 0, 1, 4)
        main_layout.addWidget(pen_width_Label, 3, 1)
        main_layout.addWidget(pen_width_SpinBox, 3, 2)
        main_layout.addWidget(approximation_step_Label, 4, 1)
        main_layout.addWidget(approximation_step_SpinBox, 4, 2)
        main_layout.addWidget(radius_Label, 5, 1)
        main_layout.addWidget(radius_SpinBox, 5, 2)
        main_layout.addWidget(x_rotate_Label, 6, 1)
        main_layout.addWidget(x_rotate_Slider, 6, 2)
        main_layout.addWidget(y_rotate_Label, 7, 1)
        main_layout.addWidget(y_rotate_Slider, 7, 2)
        main_layout.addWidget(z_rotate_Label, 8, 1)
        main_layout.addWidget(z_rotate_Slider, 8, 2)

        main_layout.addWidget(x_move_Label, 3, 3)
        main_layout.addWidget(x_move_Slider, 3, 4)
        main_layout.addWidget(y_move_Label, 4, 3)
        main_layout.addWidget(y_move_Slider, 4, 4)
        main_layout.addWidget(z_move_Label, 5, 3)
        main_layout.addWidget(z_move_Slider, 5, 4)

        main_layout.addWidget(x_scale_Label, 6, 3)
        main_layout.addWidget(x_scale_Slider, 6, 4)
        main_layout.addWidget(y_scale_Label, 7, 3)
        main_layout.addWidget(y_scale_Slider, 7, 4)
        main_layout.addWidget(z_scale_Label, 8, 3)
        main_layout.addWidget(z_scale_Slider, 8, 4)

        main_layout.addWidget(frontal_Button, 3, 5)
        main_layout.addWidget(horizontal_Button, 4, 5)
        main_layout.addWidget(profile_Button, 5, 5)

        main_layout.addWidget(isometric_Button, 3, 6)
        main_layout.addWidget(fi_angle_Label, 4, 6)
        main_layout.addWidget(fi_angle_SpinBox, 4, 7)
        main_layout.addWidget(psi_angle_Label, 5, 6)
        main_layout.addWidget(psi_angle_SpinBox, 5, 7)

        main_layout.addWidget(cabinet_Button, 3, 7)
        main_layout.addWidget(alpha_angle_Label, 4, 8)
        main_layout.addWidget(alpha_angle_SpinBox, 4, 9)
        main_layout.addWidget(L_Label, 5, 7)
        main_layout.addWidget(L_SpinBox, 5, 8)

        main_layout.addWidget(perspective_Button, 3, 8)
        main_layout.addWidget(teta_angle_Label, 4, 8)
        main_layout.addWidget(teta_angle_SpinBox, 4, 9)
        main_layout.addWidget(pfi_angle_Label, 5, 8)
        main_layout.addWidget(pfi_angle_SpinBox, 5, 9)
        main_layout.addWidget(d_Label, 6, 8)
        main_layout.addWidget(d_SpinBox, 6, 9)
        main_layout.addWidget(ro_Label, 7, 8)
        main_layout.addWidget(ro_SpinBox, 7, 9)

        self.setLayout(main_layout)

        self.render_area.set_pen_width(pen_width_SpinBox.value())
        self.render_area.sphere.set_approximation_step(approximation_step_SpinBox.value())
        self.render_area.sphere.set_radius(radius_SpinBox.value())

        self.setWindowTitle("Аппроксимация сферы")

    @staticmethod
    def create_slider(value, minimum, maximum, single_step, page_step, tick_interval):
        """
        Создаёт и настраивает слайдер для формы
        :param value:
        :param minimum:
        :param maximum:
        :param single_step:
        :param page_step:
        :param tick_interval:
        :return: QSlider
        """
        slider = QSlider(Qt.Horizontal)

        slider.setValue(value)
        slider.setRange(minimum, maximum)
        slider.setSingleStep(single_step)
        slider.setPageStep(page_step)
        slider.setTickInterval(tick_interval)
        slider.setTickPosition(QSlider.TicksRight)

        return slider

    @staticmethod
    def create_spinbox(value, minimum, maximum):
        """
        Создаёт и настраивает спинбокс для формы
        :return: QSpinBox
        """
        spinbox = QSpinBox()

        spinbox.setValue(value)
        spinbox.setRange(minimum, maximum)

        return spinbox
