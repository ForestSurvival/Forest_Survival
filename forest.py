"""
Модуль леса
"""

import math

from pygame.draw import *
from random import *

from apple import Apple


class Forest(object):
    """
    Описывает лес
    """

    def __init__(self, hero, screen):
        """
        Параметры

        Координаты центров объектов
        Словарь прямой состоит из названия оси, которой она перпендикулярна, и её координаты

        hero - объект героя
        screen - экран pygame
        """

        # Графика
        self.border_color: tuple = (185, 250, 250)  # Цвет границ
        self.border_width: int = 1  # Толщина границ в [px]
        self.color: tuple = (193, 86, 217)  # Цвет леса
        self.screen = screen

        # Логика
        self.scale: int = 35  # Масштаб в [px/м]
        self.max_draw_distance = None  # Максимальное расстояние прорисовки в [м] определяется в forest.setup()
        self.items_list: list = []  # Список объектов

        # Физика
        self.borders_dict = None  # Словари границ определяется в forest.setup()
        self.max_x_distance = None  # Горизонтальный размер экрана в [м] определяется в forest.setup()
        self.max_y_distance = None  # Вертикальный размер экрана в [м] определяется в forest.setup()

        # Объекты
        self.hero = hero

    # --- Логика ---
    def convert_horizontal_m_to_px(self, coordinate_m: float):
        """
        Преобразует [м] в [px] по горизонтали

        coordinate_m - координата объекта в [м]
        """

        distance_m: float = coordinate_m - self.hero.x  # Расстояние от героя до объекта в [м]
        distance_raw: float = distance_m * self.scale  # Расстояние в [px]
        distance_px: int = round(distance_raw)  # Округлённое расстояние в [px]
        distance_px_cooked: int = distance_px + self.screen.get_width() // 2  # Координата  объекта в [px]
        return distance_px_cooked

    def convert_vertical_m_to_px(self, coordinate_m: float):
        """
        Преобразует [м] в [px] по вертикали

        coordinate_m - координата объекта в [м]
        """

        distance_m: float = coordinate_m - self.hero.y  # Расстояние от героя до объекта в [м]
        distance_raw: float = distance_m * self.scale  # Расстояние в [px]
        distance_px: int = round(distance_raw)  # Округлённое расстояние в [px]
        distance_px_cooked: int = distance_px + self.screen.get_height() // 2  # Координата  объекта в [px]
        return distance_px_cooked

    def count_draw_distance(self):
        """
        Вычисляет расстояние прорисовки в [м]
        """

        screen_height: int = self.screen.get_height()  # Высота экрана в [px]
        screen_width: int = self.screen.get_width()  # Ширина экрана в [px]

        # Максимальное расстояние на экране в [px]
        max_screen_distance: float = math.sqrt(screen_height ** 2 + screen_width ** 2)

        max_distance: float = max_screen_distance / self.scale  # Максимальное расстояние до видимого объекта в [м]
        self.max_draw_distance: int = math.ceil(max_distance)  # Максимальное расстояние прорисовки в []

    def process_hero_actions(self):
        """
        Обрабатывает действия героя
        """

        if self.hero.status == 'acting':  # Если герой выполняет действие
            for item in self.items_list:

                # Список компонент расстояния до объекта в [м]
                distance_list: list = self.calculate_distance_to_point(item.x, item.y)

                # Расстояние до объекта в [м]
                distance: float = math.sqrt(distance_list[0] ** 2 + distance_list[1] ** 2)

                if distance <= self.hero.action_radius:
                    item.process_action(self, self.hero)

    def setup(self):
        """
        Действия при создании леса
        """

        self.create_borders()
        self.count_max_distance()
        self.count_draw_distance()
        self.generate_items()

    # --- Физика ---
    def calculate_distance_to_line(self, line_dict: dict):
        """
        Вычисляет расстояние от героя до прямой

        line_dict - словарь прямой
        """

        coordinate_dict: dict = {'x': self.hero.x,  # Словарь координат
                                 'y': self.hero.y}
        coordinate: str = line_dict['coordinate']  # Координата, вдоль которой надо считать расстяние
        hero_coordinate: float = coordinate_dict[coordinate]  # Координата x героя в [м]
        distance: float = line_dict['value'] - hero_coordinate  # Расстояние от героя до прямой в [м]
        return distance

    def calculate_distance_to_point(self, x: float, y: float):
        """
        Вычисляет компоненты расстояния от героя до точки

        x - Координата x точки в [м]
        y - Координата y точки в [м]
        """

        x_distance: float = x - self.hero.x  # Расстояние от героя до точки вдоль оси x в [м]
        y_distance: float = y - self.hero.y  # Расстояние от героя до точки вдоль оси y в [м]
        distance_list: list = [x_distance, y_distance]  # Компоненты расстояния от героя до точки в [м]
        return distance_list

    def count_max_distance(self):
        """
        Вычисляет размеры экрана в [м]
        """

        down_border_dict: dict = self.borders_dict['down']  # Словарь нижней границы
        left_border_dict: dict = self.borders_dict['left']  # Словарь левой границы
        right_border_dict: dict = self.borders_dict['right']  # Словарь правой границы
        up_border_dict: dict = self.borders_dict['up']  # Словарь верхней границы
        x_left: float = left_border_dict['value']  # Координата x левой границы в [м]
        x_right: float = right_border_dict['value']  # Координата x правой границы в [м]
        y_down: float = down_border_dict['value']  # Координата y нижней границы в [м]
        y_up: float = up_border_dict['value']  # Координата y верхней границы в [м]
        self.max_x_distance: float = x_right - x_left  # Расстояние между границами вдоль оси x в [м]
        self.max_y_distance: float = y_down - y_up  # Расстояние между границами по y в [м]

    def create_borders(self):
        """
        Создаёт словарь границ
        """

        down_border_dict: dict = {'coordinate': 'y',
                                  'value': 10}  # Словарь нижней границы леса
        left_border_dict: dict = {'coordinate': 'x',
                                  'value': -10}  # Словаь левой границы леса
        right_border_dict: dict = {'coordinate': 'x',
                                   'value': 10}  # Словарь правой границы леса
        up_border_dict: dict = {'coordinate': 'y',
                                'value': -10}  # Словарь верхней границы леса
        self.borders_dict: dict = {'down': down_border_dict,  # Словарь границ
                                   'left': left_border_dict,
                                   'right': right_border_dict,
                                   'up': up_border_dict}

    def draw_needed(self, distance: float):
        """
        Проверяет, нужно ли рисовать объект

        line_dict - словарь прямой
        """

        if distance <= self.max_draw_distance:  # Если прямую надо прорисовывать
            return True
        else:
            return False

    # --- Объекты ---
    def generate_items(self):
        """
        Создаёт объекты
        """

        apples_amount: int = 5  # Количество яблок
        for apple_number in range(apples_amount):

            # Координата x яблока в [м]
            x_apple: float = random() * self.max_x_distance + self.borders_dict['left']['value']

            # Координата y яблока в [м]
            y_apple: float = random() * self.max_y_distance + self.borders_dict['up']['value']

            apple = Apple(self.screen, x_apple, y_apple)  # Объект яблока
            self.items_list.append(apple)

    # --- Графика ---
    def draw_background(self):
        """
        Рисует фон леса
        """

        self.screen.fill(self.color)

    def draw_borders(self):
        """
        Рисует границы
        """

        for border_direction in self.borders_dict:
            border_dict: dict = self.borders_dict[border_direction]  # Словарь границы
            border_distance: float = self.calculate_distance_to_line(border_dict)  # Расстояние до границы в [м]
            if self.draw_needed(border_distance):
                coordinate_m = border_dict['value']  # Координата границы в [м]
                axis: str = border_dict['coordinate']  # Ось, вдоль которой рисовать границу
                if axis == 'x':  # Если прямая горизонтальна
                    coordinate_px: int = self.convert_horizontal_m_to_px(coordinate_m)  # Координата границы в [px]
                    self.draw_horizontal_line(coordinate_px)
                elif axis == 'y':  # Если прямая вертикальна
                    coordinate_px: int = self.convert_vertical_m_to_px(coordinate_m)  # Координата границы в [px]
                    self.draw_vertical_line(coordinate_px)

    def draw_horizontal_line(self, line_coordinate: float):
        """
        Рисует горизонтальную прямую

        line_coordinate - Координата прямой в [м]
        """

        y_1: int = -1  # Верхняя точка выше экрана
        y_2: int = self.screen.get_height() + 1  # Нижняя точка ниже экрана

        line(self.screen, self.border_color, [line_coordinate, y_1], [line_coordinate, y_2], self.border_width)

    def draw_items(self):
        """
        Рисует объекты
        """

        for item in self.items_list:
            item_x: int = self.convert_horizontal_m_to_px(item.x)  # Координата объекта по оси x в [px]
            item_y: int = self.convert_vertical_m_to_px(item.y)  # Координата объекта по оси y в [px]
            item.draw(item_x, item_y)

    def draw_vertical_line(self, line_coordinate: float):
        """
        Рисует вертикальную прямую

        line_coordinate - Координата прямой в [м]
        """

        x_1: int = -1  # Левая точка левее экрана
        x_2: int = self.screen.get_width() + 1  # Правая точка правее экрана

        line(self.screen, self.border_color, [x_1, line_coordinate], [x_2, line_coordinate], self.border_width)

    # --- Обработка ---
    def process(self):
        """
        Обрабатывает события леса
        """

        self.process_hero_actions()
        self.draw_background()
        self.draw_borders()
        self.draw_items()
