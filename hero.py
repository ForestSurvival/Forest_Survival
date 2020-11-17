"""
Модуль героя
"""

import math
import pygame

from pygame.draw import *


class Hero(object):
    """
    Описывает героя
    """

    def __init__(self, game, screen):
        """
        Параметры

        Координаты центров объектов

        game - объект игры
        screen - экран pygame
        """

        # Физика
        self.speed_max: float = 2  # Максимальная скорость героя в [м/с]
        self.x: float = 0  # Координата x героя в [м]
        self.y: float = 0  # Координата y героя в [м]

        # Логика
        self.action_radius: float = 0.5  # Расстояние, в пределах которого герой может действовать на объект в [м]
        self.keys_amount = None  # Количество клавиш на клавиатуре определяется в hero.setup()
        self.keys_pressed_list = None  # Список кнопок, которые обрабатываются определяется в hero.setup()
        self.latest_keys_pressed_list = None  # Список клавиш, нажатых квант времени назад опеделяется в hero.setup()
        self.satiety: float = 4186800  # Пищевая энергия в [Дж]
        self.satiety_max: int = 8373600  # Максимальня пищевая энергия в [Дж]
        self.satiety_reduce: int = self.satiety_max // game.day_length  # Скорость голодания в [Дж/с]
        self.status: str = 'alive'  # Герой жив

        # Объекты
        self.game = game

        # Графика
        self.color: tuple = (206, 181, 75)  # Цвет героя
        self.radius: int = 5  # Радиус в [px]
        self.screen = screen

    # --- Логика ---
    @staticmethod
    def calculate_speed_reduce(directions_list: list):
        """
        Вычисляет фактор уменьшения скорости

        directions_list - список направлений, по которым сейчас движется герой
        """

        directions_count: int = len(directions_list)  # Количество направлений, по которым сейчас идёт герой
        if directions_count == 2:  # Если герой идёт сразу по 2 направлениям
            speed_reduce: float = math.sqrt(2)  # Сохранение полной скорости героя
        else:
            speed_reduce: float = 1  # Сохранение полной скорости героя
        return speed_reduce

    def check_live_parameters(self):
        """
        Проверяет жизненно важные параметры героя
        """

        if self.satiety == 0:  # Если герой смертельно голоден
            self.get_dead()
        else:
            self.status: str = 'alive'  # Герой жив

    def count_keys_amount(self):
        """
        Считает количесто клавиш на клавиатуре
        """

        test_keys_list: list = pygame.key.get_pressed()  # Пробный список клавиш
        self.keys_amount: int = len(test_keys_list)  # Количество клавиш на клавиатуре

    def create_keys_lists(self):
        """
        Инициализирует списки обрабатываемых клавиш
        """

        self.keys_pressed_list: list = [0] * self.keys_amount  # Список обрабатываемых сейчас клавиш
        self.latest_keys_pressed_list = [0] * self.keys_amount  # Изначально не одна клавиши не нажата

    def get_dead(self):
        """
        Убивает героя
        """

        self.status: str = 'dead'  # Герой мёртв
        self.game.finish()

    def process_keys_action(self):
        """
        Обрабатывает информацию о нажатых клавишах действий
        """

        if self.keys_pressed_list[pygame.K_e] == 1:  # Если нажата клавиша E
            self.status: str = 'acting'  # Герой выполняет действие
        else:
            self.status: str = 'alive'  # Герой просто живёт

    def process_keys_motion(self):
        """
        Обрабатывает информацию о нажатых клавишах перемещения
        """

        directions_dict: dict = {pygame.K_w: 'up',  # Словарь направлений
                                 pygame.K_a: 'left',
                                 pygame.K_s: 'down',
                                 pygame.K_d: 'right'}
        directions_list: list = []  # Список направлений, по которым сейчас идёт герой
        for key in directions_dict:
            if self.keys_pressed_list[key] == 1:  # Если нажата клавиша перемещения
                directions_list.append(directions_dict[key])
        speed_reduce: float = self.calculate_speed_reduce(directions_list)  # Фактор уменьшения скорости
        actual_speed: float = self.speed_max / speed_reduce  # Действительая скорость героя в [м/с]

        for direction in directions_list:
            self.move(direction, actual_speed)

    def setup(self):
        """
        Действия при создании героя
        """

        self.count_keys_amount()
        self.create_keys_lists()

    def update_keys_pressed(self):
        """
        Обновляет информацию о нажатых клавишах
        """

        # Список клавиш, которые могут быть нажаты непрерывно
        continuous_keys_list: list = [pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w]

        current_keys_pressed_list: list = pygame.key.get_pressed()  # Список нажатых в текущий момент клавиш
        for key_index in range(self.keys_amount):
            if key_index not in continuous_keys_list:

                # Если клавиша нажата только сейчас
                if current_keys_pressed_list[key_index] == 1 and self.latest_keys_pressed_list[key_index] == 0:
                    self.keys_pressed_list[key_index] = 1  # Кнопка нажата
                else:
                    self.keys_pressed_list[key_index] = 0  # Кнопка не нажата
            else:
                # Непрерывная обработка особых клавиш
                self.keys_pressed_list[key_index] = current_keys_pressed_list[key_index]

        self.latest_keys_pressed_list: list = current_keys_pressed_list  # Обновленеие списка нажатых клавиш

    # --- Физика ---
    def get_hungry(self):
        """
        Уменьшает сытость
        """

        delta_satiety: float = self.satiety_reduce * self.game.time_step  # Квант голодания в [Дж]
        new_satiety: float = self.satiety - delta_satiety  # Новая пищевая энергия в [Дж]
        new_satiety_int: int = round(new_satiety)  # Округлённое значение новой пищевой энергии в [Дж]
        self.satiety = max(0, new_satiety_int)  # Пищевая энергия не может быть отрицательной

    def move(self, direction: str, speed: float):
        """
        Перемещает героя

        direction - направление перемещения
        speed - скорость героя
        """

        delta_distance: float = speed * self.game.time_step  # Квант перемещения в [м]

        if direction == 'up':  # Если герой идёт вверх
            self.y -= delta_distance  # Координата y героя в [м]
        if direction == 'left':  # Если герой идёт влево
            self.x -= delta_distance  # Координата x героя в [м]
        if direction == 'down':  # Если герой идёт вниз
            self.y += delta_distance  # Координата y героя в [м]
        if direction == 'right':  # Если герой идёт вправо
            self.x += delta_distance  # Координата x героя в [м]

    # --- Графика ---
    def draw(self):
        """
        Нарисовать героя
        """

        x: int = self.screen.get_width() // 2  # Координата x героя на экране в [px]
        y: int = self.screen.get_height() // 2  # Координата y героя на экране в [px]

        circle(self.screen, self.color, (x, y), self.radius)

    # --- Обработка ---
    def log(self):
        """
        Выводит информацию о герое в консоль для отладки
        """

        if self.status == 'acting':  # Если герой действует
            print(self.status)
        print('--- Game cycle ---')

    def process(self):
        """
        Обрабатывает события героя
        """

        self.get_hungry()
        self.check_live_parameters()
        self.update_keys_pressed()
        self.process_keys_action()
        self.process_keys_motion()
        self.draw()

        # Отладка
        # self.log()
