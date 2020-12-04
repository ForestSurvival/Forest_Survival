"""
Модуль героя
"""

import math
import pygame

from pygame.draw import *

from apple import Apple
from campfire import Campfire
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
        self.heat_capacity: float = 3470  # Теплоёмкость героя в [Дж / К]
        self.speed_max: float = 2  # Максимальная скорость героя в [м/с]
        self.temperature: float = 309.6  # Температура героя в [К]
        self.thermal_conductivity: float = 0.48  # Коэффициент теплопередачи в [Вт / К]
        self.thirst: float = 0.0009  # Жажда героя в [м^3]
        self.thirst_max: float = 0.0018  # Максимальная жажда героя в [м^3]
        self.thirst_increase: float = self.thirst_max / game.day_length  # Скорость увеличения жажды в [м^3/с]
        self.x: float = 0  # Координата x героя в [м]
        self.y: float = 0  # Координата y героя в [м]

        # Логика
        self.actions_moment_dict: dict = {None: None}  # Словарь мгновенных действий определяется в hero.setup()
        self.actions_current_dict: dict = {None: None}  # Словарь продолжительных действий определяется в hero.setup()
        self.action_radius: float = 0.5  # Расстояние, в пределах которого герой может действовать на объект в [м]
        self.satiety: float = 4186.8  # Пищевая энергия в [Дж]
        self.satiety_max: float = 8373.6  # Максимальня пищевая энергия в [Дж]
        self.satiety_reduce: float = self.satiety_max / game.day_length  # Скорость голодания в [Дж/с]
        self.status_current: str = 'walk'  # Герой может перемещаться
        self.status_last: str = 'walk'  # Статус героя в предыдущем цикле

        # Объекты
        self.game = game
        self.indicator_satiety = None  # Объект индикатора сытости определяется в hero.setup()
        self.indicator_thirst = None  # Объект индикатора жажды определяется в hero.setup()
        self.inventory = Inventory(self)  # Объект инвентаря

        # Графика
        self.color: tuple = (206, 181, 75)  # Цвет героя
        self.draw_list: list = [None]  # Графический список
        self.radius: int = 5  # Радиус в [px]
        # self.screen = game.graphic_engine.screen

    # --- Инициализация ---
    def set_indicator_satiety(self):
        """
        Создаёт индикатор сытости
        """

        indicator_satiety_x: int = 0  # Координата x индикатора сытости
        indicator_satiety_y: int = 0  # Координата y индикатора сытости
        satiety_percent: float = 100 * self.satiety / self.satiety_max  # Сытость героя в [%]
        self.indicator_satiety = Indicator('Сытость', self, satiety_percent, indicator_satiety_x, indicator_satiety_y)

    def set_indicator_thirst(self):
        """
        Создаёт индикатор жажды
        """

        indicator_thirst_x: int = 200  # Координата x индикатора жажды
        indicator_thirst_y: int = 0  # Координата y индикатора жажды
        thirst_percent: float = 100 * self.thirst / self.thirst_max  # Жажда героя в [%]
        self.indicator_thirst = Indicator('Жажда', self, thirst_percent, indicator_thirst_x, indicator_thirst_y)

    def setup(self):
        """
        Действия при создании героя
        """

        self.inventory.setup()
        self.set_actions_dicts()
        self.set_indicator_satiety()
        self.set_indicator_thirst()

    # --- Логика ---
    def act(self):
        """
        Герой производит действие
        """

        self.status_current: str = 'act'  # Герой производит действие

    def calculate_speed_reduce(self):
        """
        Вычисляет фактор уменьшения скорости
        """

        # Логика
        directions_count: int = 0

        if self.game.logic_engine.keys_current_list[pygame.K_w]:
            directions_count += 1
        if self.game.logic_engine.keys_current_list[pygame.K_a]:
            directions_count += 1
        if self.game.logic_engine.keys_current_list[pygame.K_s]:
            directions_count += 1
        if self.game.logic_engine.keys_current_list[pygame.K_d]:
            directions_count += 1
        if directions_count == 2:  # Если герой идёт сразу по 2 направлениям
            speed_reduce: float = math.sqrt(2)  # Сохранение полной скорости героя
        else:
            speed_reduce: float = 1  # Сохранение полной скорости героя
        return speed_reduce

    def eat_apple(self):
        """
        Герой ест яблоко
        """

        if self.inventory.apples_amount > 0 and self.satiety < self.satiety_max:  # Если есть яблоки и герой хочет есть
            apple = Apple(self.game.graphic_engine.screen, 0, 0)  # Тестовое яблоко
            self.inventory.apples_amount -= 1  # Уменьшить количество яблок в инвентаре
            self.satiety += apple.satiety

    def get_dead(self):
        """
        Убивает героя
        """

        self.status_current: str = 'dead'  # Герой мёртв
        self.game.status = 'menu'  # Перевести игру в меню
        self.game.exit()

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

    def update_status(self):
        """
        Обновляет статус героя
        """

        if self.status_current == 'act':  # Если герой выполнил действие
            if self.status_last == 'act':  # Если герой выполнил действие в предыдущем цикле
                self.status_current: str = 'walk'  # Герой может перемещаться
        self.status_last: str = self.status_current  # Обновить статус

    # --- Физика ---
    def burn_campfire(self):
        """
        Развести костёр
        """

        if self.inventory.matches_amount >= self.inventory.campfire.matches_amount:  # Если хватает спичек
            if self.inventory.paper_amount >= self.inventory.campfire.paper_amount:  # Если хватает бумаги
                if self.inventory.sticks_amount >= self.inventory.campfire.sticks_amount:  # Если хватает палок
                    campfire = Campfire(self.inventory, self.x, self.y)  # Объект костра
                    campfire.setup()
                    self.game.forest.campfires_list.append(campfire)
                    self.inventory.matches_amount -= self.inventory.campfire.matches_amount  # Спички израсходованы
                    self.inventory.paper_amount -= self.inventory.campfire.paper_amount  # Бумага израсходована
                    self.inventory.sticks_amount -= self.inventory.campfire.sticks_amount  # Палки израсходованы

    def check_live_parameters(self):
        """
        Проверяет жизненно важные параметры героя
        """

        if self.satiety == 0 or self.thirst == self.thirst_max:  # Если герой смертельно голоден или хочет пить
            self.get_dead()

    def drink_water(self):
        """
        Герой пьёт воду
        """

        if self.inventory.water_amount > 0:  # Если в инвентаре есть вода
            if self.thirst > 0:  # Если герой хочет пить
                self.thirst: float = max(self.thirst - self.inventory.water.volume, 0)  # Жажда героя уменьшается
                self.inventory.water_amount -= 1  # Вода тратится

    def get_hungry(self):
        """
        Уменьшает сытость
        """

        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_satiety: float = self.satiety_reduce * time_step  # Квант голодания в [Дж]
        new_satiety: float = self.satiety - delta_satiety  # Новая пищевая энергия в [Дж]
        new_satiety_int: int = round(new_satiety)  # Округлённая новая пищевая энергия в [Дж]
        self.satiety = max(0, new_satiety_int)  # Пищевая энергия не может быть отрицательной

    def get_inventory(self):
        """
        Отображает инвентарь
        """

        self.status_current: str = 'inventory'  # Отобразить инвентарь

    def get_thirsty(self):
        """
        Увеличивает жажду
        """

        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_thirst: float = self.thirst_increase * time_step  # Квант увеличения жажды в [м^3]
        new_thirst: float = self.thirst + delta_thirst  # Новая жажда в [м^3]
        self.thirst = min(new_thirst, self.thirst_max)  # Жажда не может быть больше максимальной

    def move_down(self):
        """
        Перемещает героя вниз
        """

        speed_reduce: float = self.calculate_speed_reduce()
        speed_actual: float = self.speed_max / speed_reduce
        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_distance: float = speed_actual * time_step  # Квант перемещения в [м]
        self.y += delta_distance  # Координата y героя в [м]

    def move_left(self):
        """
        Перемещает героя влево
        """

        speed_reduce: float = self.calculate_speed_reduce()
        speed_actual: float = self.speed_max / speed_reduce
        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_distance: float = speed_actual * time_step  # Квант перемещения в [м]
        self.x -= delta_distance  # Координата y героя в [м]

    def move_right(self):
        """
        Перемещает героя вправо
        """

        speed_reduce: float = self.calculate_speed_reduce()
        speed_actual: float = self.speed_max / speed_reduce
        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_distance: float = speed_actual * time_step  # Квант перемещения в [м]
        self.x += delta_distance  # Координата y героя в [м]

    def move_up(self):
        """
        Перемещает героя вверх
        """

        speed_reduce: float = self.calculate_speed_reduce()
        speed_actual: float = self.speed_max / speed_reduce
        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_distance: float = speed_actual * time_step  # Квант перемещения в [м]
        self.y -= delta_distance  # Координата y героя в [м]

    def update_indicator_satiety(self):
        """
        Обновляет значение индикатора сытости
        """

        satiety_percent: float = 100 * self.satiety / self.satiety_max  # Сытость героя в [%]
        self.indicator_satiety.value = satiety_percent

    def update_indicator_thirst(self):
        """
        Обновляет значение индикатора жажды
        """

        thirst_percent: float = 100 * self.thirst / self.thirst_max  # Жажда героя в [%]
        self.indicator_thirst.value = thirst_percent

    # --- Графика ---
    def draw(self):
        """
        Нарисовать героя
        """

        x: int = self.game.graphic_engine.screen.get_width() // 2  # Координата x героя на экране в [px]
        y: int = self.game.graphic_engine.screen.get_height() // 2  # Координата y героя на экране в [px]

        circle(self.game.graphic_engine.screen, self.color, (x, y), self.radius)

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

        self.get_hungry()
        self.get_thirsty()
        self.check_live_parameters()
        self.update_status()
        self.update_indicator_satiety()
        self.update_indicator_thirst()

    def process(self):
        """
        Обрабатывает события героя
        """
        self.manage_logic()
        self.manage_physics()
        self.manage_graphics()
        self.indicator_satiety.process()
        self.indicator_thirst.process()
