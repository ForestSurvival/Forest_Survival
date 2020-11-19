"""
Модуль героя
"""

import math
import pygame

from pygame.draw import *

from apple import Apple
from indicator import Indicator
from inventory import Inventory


class Hero(object):
    """
    Описывает героя
    """

    def __init__(self, game):
        """
        Параметры

        game - объект игры
        """

        # Физика
        self.speed_actual: float = 2  # Действительная скорость героя в [м/с]
        self.speed_max: float = 2  # Максимальная скорость героя в [м/с]
        self.x: float = 0  # Координата x героя в [м]
        self.y: float = 0  # Координата y героя в [м]

        # Логика
        self.actions_moment_dict: dict = {None: None}  # Словарь мгновенных действий определяется в hero.setup()
        self.actions_current_dict: dict = {None: None}  # Словарь продолжительных действий определяется в hero.setup()
        self.action_radius: float = 0.5  # Расстояние, в пределах которого герой может действовать на объект в [м]
        self.satiety: float = 4186.8  # Пищевая энергия в [Дж]
        self.satiety_max: float = 8373.6  # Максимальня пищевая энергия в [Дж]
        self.satiety_reduce: int = self.satiety_max // game.day_length  # Скорость голодания в [Дж/с]
        self.status_current: str = 'walk'  # Герой может перемещаться
        self.status_last: str = 'walk'  # Статус героя в предыдущем цикле

        # Объекты
        self.game = game
        self.indicator_satiety = None  # Объект индикатора сытости определяется в hero.setup()
        self.inventory = Inventory(self)  # Объект инвентаря

        # Графика
        self.color: tuple = (206, 181, 75)  # Цвет героя
        self.draw_list: list = [None]  # Графический список
        self.radius: int = 5  # Радиус в [px]
        self.screen = game.screen

    # --- Инициализация ---
    def setup(self):
        """
        Действия при создании героя
        """

        self.inventory.setup()
        self.set_actions_dicts()
        self.set_indicator_satiety()

    # --- Логика ---
    def act(self):
        """
        Герой производит действие
        """

        self.status_current: str = 'act'  # Герой производит действие

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

    def eat_apple(self):
        """
        Герой ест яблоко
        """

        if self.inventory.apples_amount > 0 and self.satiety < self.satiety_max:  # Если есть яблоки и герой хочет есть
            apple = Apple(self.game.screen, 0, 0)  # Тестовое яблоко
            self.inventory.apples_amount -= 1  # Уменьшить количество яблок в инвентаре
            self.satiety += apple.satiety

    def get_dead(self):
        """
        Убивает героя
        """

        self.status_current: str = 'dead'  # Герой мёртв
        self.game.finish()

    def set_actions_dicts(self):
        """
        Создаёт словарь действий
        """

        self.actions_moment_dict: dict = {pygame.K_e: self.act,  # Словарь мгновенных действий
                                          pygame.K_ESCAPE: self.walk,
                                          pygame.K_i: self.get_inventory}
        self.actions_current_dict: dict = {pygame.K_a: self.move_left,
                                           pygame.K_d: self.move_right,
                                           pygame.K_s: self.move_down,
                                           pygame.K_w: self.move_up}  # Словарь продолжительных действий

    def set_indicator_satiety(self):
        """
        Обновляет индикатор сытости
        """

        indicator_satiety_x: int = 0  # Координата x индикатора сытости
        indicator_satiety_y: int = 0  # Координата y индикатора сытости
        satiety_percent: float = 100 * self.satiety / self.satiety_max  # Сытость героя в [%]
        self.indicator_satiety = Indicator('Сытость', self, satiety_percent, indicator_satiety_x, indicator_satiety_y)

    def walk(self):
        """
        Позволяет герою перемещаться
        """

        self.status_current: str = 'walk'

    def update_draw_list(self):
        """
        Обновляет графический список
        """

        if self.status_current == 'act':  # Если герой выполняет действие
            self.draw_list: list = [self.draw]  # Рисовать героя
        elif self.status_current == 'inventory':  # Если герой просматривает инвентарь
            self.draw_list: list = [None]  # Ничего не рисовать
        elif self.status_current == 'walk':  # Если герой может перемещаться
            self.draw_list: list = [self.draw]  # Рисовать героя
        else:
            self.draw_list: list = [None]  # Ничего не рисоваь

    def update_indicator_satiety(self):
        """
        Обновляет значение индикатора сытости
        """

        satiety_percent: float = 100 * self.satiety / self.satiety_max  # Сытость героя в [%]
        self.indicator_satiety.value = satiety_percent

    def update_status(self):
        """
        Обновляет статус героя
        """

        if self.status_current == 'act':  # Если герой выполнил действие
            if self.status_last == 'act':  # Если герой выполнил действие в предыдущем цикле
                self.status_current: str = 'walk'  # Герой может перемещаться
        self.status_last: str = self.status_current  # Обновить статус

    # --- Физика ---
    def get_hungry(self):
        """
        Уменьшает сытость
        """

        delta_satiety: float = self.satiety_reduce * self.game.time_step  # Квант голодания в [Дж]
        new_satiety: float = self.satiety - delta_satiety  # Новая пищевая энергия в [Дж]
        new_satiety_int: int = round(new_satiety)  # Округлённое значение новой пищевой энергии в [Дж]
        self.satiety = max(0, new_satiety_int)  # Пищевая энергия не может быть отрицательной

    def get_inventory(self):
        """
        Отображает инвентарь
        """

        self.status_current: str = 'inventory'  # Отобразить инвентарь

    def move_down(self):
        """
        Перемещает героя вниз
        """

        delta_distance: float = self.speed_actual * self.game.time_step  # Квант перемещения в [м]
        self.y += delta_distance  # Координата y героя в [м]

    def move_left(self):
        """
        Перемещает героя влево
        """

        delta_distance: float = self.speed_actual * self.game.time_step  # Квант перемещения в [м]
        self.x -= delta_distance  # Координата y героя в [м]

    def move_right(self):
        """
        Перемещает героя вправо
        """

        delta_distance: float = self.speed_actual * self.game.time_step  # Квант перемещения в [м]
        self.x += delta_distance  # Координата y героя в [м]

    def move_up(self):
        """
        Перемещает героя вверх
        """

        delta_distance: float = self.speed_actual * self.game.time_step  # Квант перемещения в [м]
        self.y -= delta_distance  # Координата y героя в [м]

    # --- Графика ---
    def draw(self):
        """
        Нарисовать героя
        """

        x: int = self.screen.get_width() // 2  # Координата x героя на экране в [px]
        y: int = self.screen.get_height() // 2  # Координата y героя на экране в [px]

        circle(self.screen, self.color, (x, y), self.radius)

    # --- Обработка ---
    def manage_graphics(self):
        """
        Обрабатывает графические события героя
        """

        self.update_draw_list()
        for draw in self.draw_list:
            if draw is not None:
                draw()

    def manage_logic(self):
        """
        Обрабатывает логические события героя
        """

        self.get_hungry()
        self.check_live_parameters()
        self.update_status()
        for key_index in range(self.game.logic_engine.keys_amount):
            if key_index in self.actions_current_dict:
                if self.game.logic_engine.keys_current_list[key_index] == 1:  # Если клавиша нажата в текущем цикле
                    self.actions_current_dict[key_index]()
            if key_index in self.actions_moment_dict:

                # Если клавиша нажата строго в текущем цикле
                if self.game.logic_engine.keys_moment_list[key_index] == 1:
                    self.actions_moment_dict[key_index]()

    def manage_physics(self):
        """
        Обрабатывает физические события героя
        """

        self.update_indicator_satiety()

    def process(self):
        """
        Обрабатывает события героя
        """

        self.manage_physics()
        self.manage_graphics()
        self.indicator_satiety.process()
