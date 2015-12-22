# ~*~ coding: utf-8 ~*~

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QHBoxLayout, QTabWidget, QSplitter, QGroupBox,
                             QSpinBox, QDoubleSpinBox, QSlider, QLabel, QRadioButton, QPushButton, QCheckBox)
from render_area import RenderArea


class Window(QWidget):
    """
    Класс пользовательского интерфейса
    """
    def __init__(self):
        super(Window, self).__init__()

        self.render_area = RenderArea()

        self.tabs = QTabWidget(self)

        """
        Управление общими параметрами сферы
        """
        # Управляющий элемент для шага аппроксимации
        self.approximation_step_SpinBox = self.create_spinbox(1, 1, 50)
        self.approximation_step_Label = QLabel("Шаг аппроксимации:")
        self.approximation_step_Label.setBuddy(self.approximation_step_SpinBox)
        # Управляющий элемент для радиуса сферы
        self.radius_SpinBox = self.create_spinbox(30, 1, 50)
        self.radius_Label = QLabel("Радиус сферы:")
        self.radius_Label.setBuddy(self.radius_SpinBox)
        # Управляющие элементы для поворотов по осям
        self.x_rotate_Label = QLabel("Поворот по оси 0X")
        self.y_rotate_Label = QLabel("Поворот по оси 0Y")
        self.z_rotate_Label = QLabel("Поворот по оси 0Z")
        self.x_rotate_Slider = self.create_slider(0, 0, 360, 1, 60, 1)
        self.y_rotate_Slider = self.create_slider(0, 0, 360, 1, 60, 1)
        self.z_rotate_Slider = self.create_slider(0, 0, 360, 1, 60, 1)
        # Управляющие элементы для перемещения по осям
        self.x_move_Label = QLabel("Перемещение по оси 0X")
        self.y_move_Label = QLabel("Перемещение по оси 0Y")
        self.z_move_Label = QLabel("Перемещение по оси 0Z")
        self.x_move_Slider = self.create_slider(0, -300, 300, 1, 60, 1)
        self.y_move_Slider = self.create_slider(0, -300, 300, 1, 60, 1)
        self.z_move_Slider = self.create_slider(0, -300, 300, 1, 60, 1)
        # Управляющие элементы для масштабирования по осям
        self.x_scale_Label = QLabel("Масштабирование по оси 0X")
        self.y_scale_Label = QLabel("Масштабирование по оси 0Y")
        self.z_scale_Label = QLabel("Масштабирование по оси 0Z")
        self.x_scale_Slider = self.create_slider(1, 1, 10, 1, 60, 1)
        self.y_scale_Slider = self.create_slider(1, 1, 10, 1, 60, 1)
        self.z_scale_Slider = self.create_slider(1, 1, 10, 1, 60, 1)

        # Наполняем первый таб для интерфейса пользователя
        self.controls_layout = QGridLayout()
        self.controls_layout.addWidget(self.approximation_step_Label, 0, 0)
        self.controls_layout.addWidget(self.approximation_step_SpinBox, 0, 1)
        self.controls_layout.addWidget(self.radius_Label, 1, 0)
        self.controls_layout.addWidget(self.radius_SpinBox, 1, 1)
        self.controls_layout.addWidget(self.x_rotate_Label, 2, 0)
        self.controls_layout.addWidget(self.x_rotate_Slider, 2, 1)
        self.controls_layout.addWidget(self.y_rotate_Label, 3, 0)
        self.controls_layout.addWidget(self.y_rotate_Slider, 3, 1)
        self.controls_layout.addWidget(self.z_rotate_Label, 4, 0)
        self.controls_layout.addWidget(self.z_rotate_Slider, 4, 1)
        self.controls_layout.addWidget(self.x_move_Label, 5, 0)
        self.controls_layout.addWidget(self.x_move_Slider, 5, 1)
        self.controls_layout.addWidget(self.y_move_Label, 6, 0)
        self.controls_layout.addWidget(self.y_move_Slider, 6, 1)
        self.controls_layout.addWidget(self.z_move_Label, 7, 0)
        self.controls_layout.addWidget(self.z_move_Slider, 7, 1)
        self.controls_layout.addWidget(self.x_scale_Label, 8, 0)
        self.controls_layout.addWidget(self.x_scale_Slider, 8, 1)
        self.controls_layout.addWidget(self.y_scale_Label, 9, 0)
        self.controls_layout.addWidget(self.y_scale_Slider, 9, 1)
        self.controls_layout.addWidget(self.z_scale_Label, 10, 0)
        self.controls_layout.addWidget(self.z_scale_Slider, 10, 1)
        self.controls_layout.setRowStretch(11, 1)

        self.controls_widget = QWidget(self)
        self.controls_widget.setLayout(self.controls_layout)

        self.tabs.addTab(self.controls_widget, "Управление")

        """
        Управление проекциями
        """
        # Управляющие элементы для переключения проекций
        self.default_projection = QRadioButton('По умолчанию')
        self.front_projection = QRadioButton('Фронтальная')
        self.horizontal_projection = QRadioButton('Горизонтальная')
        self.profile_projection = QRadioButton('Профильная')
        self.axonometric_projection = QRadioButton('Аксонометрическая')
        self.oblique_projection = QRadioButton('Косоугольная')
        self.perspective_projection = QRadioButton('Перспективная')

        self.default_projection.setObjectName("default")
        self.front_projection.setObjectName("front")
        self.horizontal_projection.setObjectName("horizontal")
        self.profile_projection.setObjectName("profile")
        self.axonometric_projection.setObjectName("axonometric")
        self.oblique_projection.setObjectName("oblique")
        self.perspective_projection.setObjectName("perspective")

        self.default_projection.setChecked(True)

        # Настройки для аксонометрической проекции
        self.axonometric_fi_angle_Label = QLabel("Угол φ:")
        self.axonometric_fi_angle_SpinBox = self.create_spinbox(40, 0, 360)
        self.axonometric_fi_angle_Label.setBuddy(self.axonometric_fi_angle_SpinBox)

        self.axonometric_psi_angle_Label = QLabel("Угол ψ:")
        self.axonometric_psi_angle_SpinBox = self.create_spinbox(10, 0, 360)
        self.axonometric_psi_angle_Label.setBuddy(self.axonometric_psi_angle_SpinBox)

        # Косоугольная
        self.oblique_alpha_angle_Label = QLabel("Угол α:")
        self.oblique_alpha_angle_SpinBox = self.create_spinbox(20, 0, 360)
        self.oblique_alpha_angle_Label.setBuddy(self.oblique_alpha_angle_SpinBox)

        self.oblique_L_Label = QLabel("L:")
        self.oblique_L_SpinBox = self.create_double_spinbox(0.1, 0.01, 0.1, 50)
        self.oblique_L_Label.setBuddy(self.oblique_L_SpinBox)

        # Перспективная
        self.perspective_teta_angle_Label = QLabel("Угол θ:")
        self.perspective_teta_angle_SpinBox = self.create_spinbox(580, -1000, 1000)
        self.perspective_teta_angle_Label.setBuddy(self.perspective_teta_angle_SpinBox)

        self.perspective_fi_angle_Label = QLabel("Угол φ:")
        self.perspective_fi_angle_SpinBox = self.create_spinbox(-5, -1000, 1000)
        self.perspective_fi_angle_Label.setBuddy(self.perspective_fi_angle_SpinBox)

        self.perspective_d_Label = QLabel("d:")
        self.perspective_d_SpinBox = self.create_spinbox(250, -1000, 1000)
        self.perspective_d_Label.setBuddy(self.perspective_d_SpinBox)

        self.perspective_ro_Label = QLabel("ρ:")
        self.perspective_ro_SpinBox = self.create_spinbox(420, -1000, 1000)
        self.perspective_ro_Label.setBuddy(self.perspective_ro_SpinBox)

        # Наполняем второй таб для интерфейса пользователя
        self.projection_layout = QGridLayout()
        self.projection_layout.addWidget(self.default_projection, 0, 0)
        self.projection_layout.addWidget(self.front_projection, 1, 0)
        self.projection_layout.addWidget(self.horizontal_projection, 2, 0)
        self.projection_layout.addWidget(self.profile_projection, 3, 0)
        self.projection_layout.addWidget(self.axonometric_projection, 4, 0)
        self.projection_layout.addWidget(self.axonometric_fi_angle_Label, 5, 0)
        self.projection_layout.addWidget(self.axonometric_fi_angle_SpinBox, 5, 1)
        self.projection_layout.addWidget(self.axonometric_psi_angle_Label, 5, 2)
        self.projection_layout.addWidget(self.axonometric_psi_angle_SpinBox, 5, 3)
        self.projection_layout.addWidget(self.oblique_projection, 6, 0)
        self.projection_layout.addWidget(self.oblique_alpha_angle_Label, 7, 0)
        self.projection_layout.addWidget(self.oblique_alpha_angle_SpinBox, 7, 1)
        self.projection_layout.addWidget(self.oblique_L_Label, 7, 2)
        self.projection_layout.addWidget(self.oblique_L_SpinBox, 7, 3)
        self.projection_layout.addWidget(self.perspective_projection, 8, 0)
        self.projection_layout.addWidget(self.perspective_teta_angle_Label, 9, 0)
        self.projection_layout.addWidget(self.perspective_teta_angle_SpinBox, 9, 1)
        self.projection_layout.addWidget(self.perspective_fi_angle_Label, 9, 2)
        self.projection_layout.addWidget(self.perspective_fi_angle_SpinBox, 9, 3)
        self.projection_layout.addWidget(self.perspective_d_Label, 10, 0)
        self.projection_layout.addWidget(self.perspective_d_SpinBox, 10, 1)
        self.projection_layout.addWidget(self.perspective_ro_Label, 10, 2)
        self.projection_layout.addWidget(self.perspective_ro_SpinBox, 10, 3)
        self.projection_layout.setRowStretch(11, 1)

        self.projection_widget = QWidget(self)
        self.projection_widget.setLayout(self.projection_layout)

        self.tabs.addTab(self.projection_widget, "Проекции")

        """
        Управление светом
        """
        # Управляющий элемент для ширины линии
        self.pen_width_SpinBox = self.create_spinbox(3, 0, 20)
        self.pen_width_Label = QLabel("Ширина линии:")
        self.pen_width_Label.setBuddy(self.pen_width_SpinBox)
        # Управляющие элементы для цвета линии
        self.pen_color_Label = QLabel("Цвет линии #000000")
        self.pen_color_Button = QPushButton("Изменить цвет линии")
        # Управляющий элемент для отсечения
        self.clipping_CheckBox = QCheckBox("Отсечение")
        self.clipping_CheckBox.setChecked(False)
        # Управляющие элементы для цвета объекта
        self.object_color_Label = QLabel("Цвет объекта #00ff00")
        self.object_color_Button = QPushButton("Изменить цвет объекта")
        # Управляющие элементы для положения источника света
        self.light_x_SpinBox = self.create_spinbox(0, -100, 100)
        self.light_x_Label = QLabel("X:")
        self.light_x_Label.setBuddy(self.light_x_SpinBox)
        self.light_y_SpinBox = self.create_spinbox(0, -100, 100)
        self.light_y_Label = QLabel("Y:")
        self.light_y_Label.setBuddy(self.light_y_SpinBox)
        self.light_z_SpinBox = self.create_spinbox(-1000, -100, 100)
        self.light_z_Label = QLabel("Z:")
        self.light_z_Label.setBuddy(self.light_z_SpinBox)
        # Группирующий элемент для управляющий светом элементов
        self.light_GroupBox = QGroupBox("Источник света")
        self.light_GroupBox.setCheckable(True)
        self.light_GroupBox_layout = QGridLayout(self)
        self.light_GroupBox_layout.addWidget(self.object_color_Label, 0, 0)
        self.light_GroupBox_layout.addWidget(self.object_color_Button, 0, 1)
        self.light_GroupBox_layout.addWidget(self.light_x_Label, 1, 0)
        self.light_GroupBox_layout.addWidget(self.light_x_SpinBox, 1, 1)
        self.light_GroupBox_layout.addWidget(self.light_y_Label, 2, 0)
        self.light_GroupBox_layout.addWidget(self.light_y_SpinBox, 2, 1)
        self.light_GroupBox_layout.addWidget(self.light_z_Label, 3, 0)
        self.light_GroupBox_layout.addWidget(self.light_z_SpinBox, 3, 1)
        self.light_GroupBox.setLayout(self.light_GroupBox_layout)

        # Наполняем третий таб для интерфейса пользователя
        self.light_layout = QGridLayout()
        self.light_layout.addWidget(self.pen_width_Label, 0, 0)
        self.light_layout.addWidget(self.pen_width_SpinBox, 0, 1)
        self.light_layout.addWidget(self.pen_color_Label, 1, 0)
        self.light_layout.addWidget(self.pen_color_Button, 1, 1)
        self.light_layout.addWidget(self.clipping_CheckBox, 2, 0)
        self.light_layout.addWidget(self.light_GroupBox, 3, 0, 1, 2)
        self.light_layout.setRowStretch(4, 1)

        self.light_widget = QWidget(self)
        self.light_widget.setLayout(self.light_layout)

        self.tabs.addTab(self.light_widget, "Свет")

        # splitter позволит пользователю изменять ширину колонок с настройками и графикой
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.render_area)

        # Основной слой - тут то, что пользователю будет показано в интерфейсе
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.splitter)
        self.setLayout(main_layout)

        self.make_widgets_connect()

        self.set_default_values()

        self.setWindowTitle("Аппроксимация сферы")

    def make_widgets_connect(self):
        """
        Осуществляет привязку сигналов от виджетов к слотам
        """
        self.pen_width_SpinBox.valueChanged.connect(self.render_area.set_pen_width)
        self.approximation_step_SpinBox.valueChanged.connect(self.render_area.sphere.set_approximation_step)
        self.radius_SpinBox.valueChanged.connect(self.render_area.sphere.set_radius)
        self.x_rotate_Slider.valueChanged.connect(self.render_area.sphere.set_x_rotate_angle)
        self.y_rotate_Slider.valueChanged.connect(self.render_area.sphere.set_y_rotate_angle)
        self.z_rotate_Slider.valueChanged.connect(self.render_area.sphere.set_z_rotate_angle)

        self.x_move_Slider.valueChanged.connect(self.render_area.sphere.set_x_move)
        self.y_move_Slider.valueChanged.connect(self.render_area.sphere.set_y_move)
        self.z_move_Slider.valueChanged.connect(self.render_area.sphere.set_z_move)

        self.x_scale_Slider.valueChanged.connect(self.render_area.sphere.set_x_scale)
        self.y_scale_Slider.valueChanged.connect(self.render_area.sphere.set_y_scale)
        self.z_scale_Slider.valueChanged.connect(self.render_area.sphere.set_z_scale)

        self.default_projection.toggled.connect(lambda: self.render_area.set_projection(self.default_projection))
        self.front_projection.toggled.connect(lambda: self.render_area.set_projection(self.front_projection))
        self.horizontal_projection.toggled.connect(lambda: self.render_area.set_projection(self.horizontal_projection))
        self.profile_projection.toggled.connect(lambda: self.render_area.set_projection(self.profile_projection))
        self.axonometric_projection.toggled.connect(lambda: self.render_area.set_projection(self.axonometric_projection))
        self.oblique_projection.toggled.connect(lambda: self.render_area.set_projection(self.oblique_projection))
        self.perspective_projection.toggled.connect(lambda: self.render_area.set_projection(self.perspective_projection))

        self.axonometric_fi_angle_SpinBox.valueChanged.connect(self.render_area.sphere.set_axonometric_angle_fi)
        self.axonometric_psi_angle_SpinBox.valueChanged.connect(self.render_area.sphere.set_axonometric_angle_psi)

        self.oblique_alpha_angle_SpinBox.valueChanged.connect(self.render_area.sphere.set_oblique_angle_alpha)
        self.oblique_L_SpinBox.valueChanged.connect(self.render_area.sphere.set_oblique_L)

        self.perspective_teta_angle_SpinBox.valueChanged.connect(self.render_area.sphere.set_perspective_angle_teta)
        self.perspective_fi_angle_SpinBox.valueChanged.connect(self.render_area.sphere.set_perspective_angle_fi)
        self.perspective_d_SpinBox.valueChanged.connect(self.render_area.sphere.set_perspective_d)
        self.perspective_ro_SpinBox.valueChanged.connect(self.render_area.sphere.set_perspective_ro)

        self.light_GroupBox.toggled.connect(lambda: self.render_area.set_light(self.light_GroupBox.isChecked(),
                                                                               self.clipping_CheckBox))
        self.clipping_CheckBox.stateChanged.connect(self.render_area.set_clipping)
        self.pen_color_Button.clicked.connect(lambda: self.render_area.set_pen_color(self.pen_color_Label))
        self.object_color_Button.clicked.connect(lambda: self.render_area.set_faces_color(self.object_color_Label))
        self.light_x_SpinBox.valueChanged.connect(self.render_area.sphere.set_light_x)
        self.light_y_SpinBox.valueChanged.connect(self.render_area.sphere.set_light_y)
        self.light_z_SpinBox.valueChanged.connect(self.render_area.sphere.set_light_z)

    def set_default_values(self):
        """
        Установка значений по умолчанию
        """
        self.render_area.sphere.set_approximation_step(self.approximation_step_SpinBox.value())
        self.render_area.sphere.set_radius(self.radius_SpinBox.value())
        self.render_area.sphere.set_x_rotate_angle(self.x_rotate_Slider.value())
        self.render_area.sphere.set_y_rotate_angle(self.y_rotate_Slider.value())
        self.render_area.sphere.set_z_rotate_angle(self.z_rotate_Slider.value())
        self.render_area.sphere.set_x_move(self.x_move_Slider.value())
        self.render_area.sphere.set_y_move(self.y_move_Slider.value())
        self.render_area.sphere.set_z_move(self.z_move_Slider.value())
        self.render_area.sphere.set_x_scale(self.x_scale_Slider.value())
        self.render_area.sphere.set_y_scale(self.y_scale_Slider.value())
        self.render_area.sphere.set_z_scale(self.z_scale_Slider.value())

        self.render_area.set_projection(self.default_projection)
        self.render_area.sphere.set_axonometric_angle_fi(self.axonometric_fi_angle_SpinBox.value())
        self.render_area.sphere.set_axonometric_angle_psi(self.axonometric_psi_angle_SpinBox.value())
        self.render_area.sphere.set_oblique_angle_alpha(self.oblique_alpha_angle_SpinBox.value())
        self.render_area.sphere.set_oblique_L(self.oblique_L_SpinBox.value())
        self.render_area.sphere.set_perspective_angle_teta(self.perspective_teta_angle_SpinBox.value())
        self.render_area.sphere.set_perspective_angle_fi(self.perspective_fi_angle_SpinBox.value())
        self.render_area.sphere.set_perspective_d(self.perspective_d_SpinBox.value())
        self.render_area.sphere.set_perspective_ro(self.perspective_ro_SpinBox.value())

        self.render_area.set_pen_width(self.pen_width_SpinBox.value())
        self.render_area.set_clipping(self.clipping_CheckBox.isChecked())
        self.render_area.sphere.set_light_x(self.light_x_SpinBox.value())
        self.render_area.sphere.set_light_y(self.light_y_SpinBox.value())
        self.render_area.sphere.set_light_z(self.light_z_SpinBox.value())

        self.light_GroupBox.setChecked(False)


    @staticmethod
    def create_slider(value, minimum, maximum, single_step, page_step, tick_interval):
        """
        Создаёт и настраивает слайдер для формы
        :param value: Значение по умолчанию
        :param minimum: Минимально допустимое значение
        :param maximum: Максимально допустимое значение
        :param single_step: Шаг, с которым изменяется слайдер от нажатия на стрелки
        :param page_step: Шаг, с которым изменяется слайдер при нажатии PageUp и PageDown
        :param tick_interval: Интервал между метками под слайдером. Если 0, то будет выбран или single_step или page_step
        :return: QSlider
        """
        slider = QSlider(Qt.Horizontal)

        slider.setRange(minimum, maximum)
        slider.setSingleStep(single_step)
        slider.setPageStep(page_step)
        slider.setTickInterval(tick_interval)
        slider.setTickPosition(QSlider.TicksRight)
        slider.setValue(value)

        return slider

    @staticmethod
    def create_spinbox(value, minimum, maximum):
        """
        Создаёт и настраивает спинбокс для формы
        :param value: Значение по умолчанию
        :param minimum: Минимально допустимое значение
        :param maximum: Максимально допустимое значение
        :return: QSpinBox
        """
        spinbox = QSpinBox()

        spinbox.setRange(minimum, maximum)
        spinbox.setValue(value)

        return spinbox

    @staticmethod
    def create_double_spinbox(value, step, minimum, maximum):
        """
        Создаёт и настраивает спинбокс с дробными значениями для формы
        :param value: Значение по умолчанию
        :param step: Шаг изменения значения
        :param minimum: Минимально допустимое значение
        :param maximum: Максимально допустимое значение
        :return: QSpinBox
        """
        spinbox = QDoubleSpinBox()

        spinbox.setSingleStep(step)
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(value)

        return spinbox

