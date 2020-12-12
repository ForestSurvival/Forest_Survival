"""
Модуль героя
"""

import math
import pygame

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
        self.heat_bonus_clothes: float = 23  # Такую температуру в [К] даёт герою одежда
        self.heat_capacity: float = 3470  # Теплоёмкость героя в [Дж / К]
        self.speed_max: float = 2.5  # Максимальная скорость героя в [м/с]
        self.temperature: float = 309.6  # Температура героя в [К]
        self.temperature_max: float = 329.6  # Максимальная температура героя в [К]
        self.temperature_min: float = 289.6  # Температурав [К], при которой герой умирает
        self.thermal_conductivity: float = 0.48  # Коэффициент теплопередачи в [Вт / К]
        self.thirst: float = 0.0009  # Жажда героя в [м^3]
        self.thirst_max: float = 0.0018  # Максимальная жажда героя в [м^3]
        self.thirst_increase: float = self.thirst_max / game.day_length  # Скорость увеличения жажды в [м^3/с]
        self.tick_count_start: int = 0  # Количесто циклов, прошедших с начала ходьбы героя в одну сторону
        self.x: float = 0  # Координата x героя в [м]
        self.y: float = 0  # Координата y героя в [м]

        # Логика
        self.actions_moment_dict: dict = {None: None}  # Словарь мгновенных действий определяется в hero.setup()
        self.actions_current_dict: dict = {None: None}  # Словарь продолжительных действий определяется в hero.setup()
        self.action_radius: float = 0.5  # Расстояние, в пределах которого герой может действовать на объект в [м]
        self.button_last: str = 'S'
        self.key: int = 0  # Номер изображения
        self.key_last = self.key
        self.satiety: float = 4186.8  # Пищевая энергия в [Дж]
        self.satiety_max: float = 8373.6  # Максимальня пищевая энергия в [Дж]
        self.satiety_reduce: float = self.satiety_max / game.day_length  # Скорость голодания в [Дж/с]
        self.status_current: str = 'walk'  # Герой может перемещаться
        self.status_last: str = 'walk'  # Статус героя в предыдущем цикле

        # Объекты
        self.game = game
        self.indicator_heat = None  # Объект индикатора теплоты определяется в hero.setup()
        self.indicator_satiety = None  # Объект индикатора сытости определяется в hero.setup()
        self.indicator_thirst = None  # Объект индикатора жажды определяется в hero.setup()
        self.inventory = Inventory(self)  # Объект инвентаря

        # Графика
        self.color: tuple = (206, 181, 75)  # Цвет героя
        self.draw_list: list = [None]  # Графический список
        self.radius: int = 5  # Радиус в [px]
        self.graphical_height: int = 36  # Графическая высота героя в [px]
        self.graphical_width: int = 30  # Графическая ширина героя в [px]

        # Изображения героя в формате bmp
        self.image_hero_dict: dict = {'W': [pygame.image.load('Sprites/Heroes/hero_up_1.bmp'),
                                            pygame.image.load('Sprites/Heroes/hero_up_2.bmp')],
                                      'S': [pygame.image.load('Sprites/Heroes/hero_down_1.bmp'),
                                            pygame.image.load('Sprites/Heroes/hero_down_2.bmp')],
                                      'A': [pygame.image.load('Sprites/Heroes/hero_left_1.bmp'),
                                            pygame.image.load('Sprites/Heroes/hero_left_2.bmp')],
                                      'D': [pygame.image.load('Sprites/Heroes/hero_right_1.bmp'),
                                            pygame.image.load('Sprites/Heroes/hero_right_2.bmp')],
                                      'WA': [pygame.image.load('Sprites/Heroes/hero_up_left_1.bmp'),
                                             pygame.image.load('Sprites/Heroes/hero_up_left_2.bmp')],
                                      'WD': [pygame.image.load('Sprites/Heroes/hero_up_right_1.bmp'),
                                             pygame.image.load('Sprites/Heroes/hero_up_right_2.bmp')],
                                      'SA': [pygame.image.load('Sprites/Heroes/hero_down_left_1.bmp'),
                                             pygame.image.load('Sprites/Heroes/hero_down_left_2.bmp')],
                                      'SD': [pygame.image.load('Sprites/Heroes/hero_down_right_1.bmp'),
                                             pygame.image.load('Sprites/Heroes/hero_down_right_2.bmp')]}

    # --- Инициализация ---
    def set_indicator_heat(self):
        """
        Создаёт индикатор температуры
        """

        # Физика
        t: float = self.temperature

        indicator_heat_x: int = 400  # Координата x индикатора температуры
        indicator_heat_y: int = 0  # Координата y индикатора температуры

        # Температура героя в [%]
        heat_percent: float = 100 * (t - self.temperature_min) / (self.temperature_max - self.temperature_min)

        self.indicator_heat = Indicator('Температура', self, heat_percent, indicator_heat_x, indicator_heat_y)

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
        self.set_indicator_heat()
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

        satiety_comfort: float = 0.9  # Если сытость больше 90 %, герой не хочет есть

        if self.inventory.apples_amount > 0:  # Если есть яблоки
            if self.satiety < self.satiety_max * satiety_comfort:  # Если герой хочет есть
                apple = Apple(self.game.graphic_engine.screen, 0, 0)  # Тестовое яблоко
                self.inventory.apples_amount -= 1  # Уменьшить количество яблок в инвентаре
                self.satiety += apple.satiety

    def get_dead_from_frost(self):
        """
        Убивает героя от переохлаждения
        """

        self.status_current: str = 'dead'  # Герой мёртв
        self.game.status = 'menu'  # Перевести игру в меню
        self.game.menu.status = 'frost'  # Сообщение о смерти

    def get_dead_from_starvation(self):
        """
        Убивает героя от голода
        """

        self.status_current: str = 'dead'  # Герой мёртв
        self.game.status = 'menu'  # Перевести игру в меню
        self.game.menu.status = 'starvation'  # Сообщение о смерти

    def get_dead_from_thirst(self):
        """
        Убивает героя от жажды
        """

        self.status_current: str = 'dead'  # Герой мёртв
        self.game.status = 'menu'  # Перевести игру в меню
        self.game.menu.status = 'thirst'  # Сообщение о смерти

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

        if self.satiety == 0:  # Если герой голоден
            self.get_dead_from_starvation()
        if self.thirst == self.thirst_max:  # Если герой испытывает жажду
            self.get_dead_from_thirst()
        if self.temperature == self.temperature_min:  # Если герой замёрх
            self.get_dead_from_frost()

    def drink_water(self):
        """
        Герой пьёт воду
        """

        thirst_comfort: float = 10  # Если жажда составляет 1/10 от максимальной, герой не хочет пить

        if self.inventory.water_amount > 0:  # Если в инвентаре есть вода
            if self.thirst > self.thirst_max / thirst_comfort:  # Если герой хочет пить
                self.thirst: float = max(self.thirst - self.inventory.water.volume, 0)  # Жажда героя уменьшается
                self.inventory.water_amount -= 1  # Вода тратится

    def get_hungry(self):
        """
        Уменьшает сытость
        """

        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_satiety: float = self.satiety_reduce * time_step  # Квант голодания в [Дж]
        new_satiety: float = self.satiety - delta_satiety  # Новая пищевая энергия в [Дж]
        self.satiety: float = max(0.0, new_satiety)  # Пищевая энергия не может быть отрицательной

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

        move_allowed: bool = True  # Разрешено ли перемещаться
        speed_reduce: float = self.calculate_speed_reduce()
        speed_actual: float = self.speed_max / speed_reduce
        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_distance: float = speed_actual * time_step  # Квант перемещения в [м]
        new_y: float = self.y + delta_distance  # Предпологаемая координата y в [м] после шага
        for tree in self.game.forest.trees_list:

            # Расстояние до центра круга коллизии дерева в [м]
            distance: float = self.game.physical_engine.get_physical_distance(self.x, new_y, tree.stop_x, tree.stop_y)
            if distance <= tree.collision_radius:
                move_allowed: bool = False  # Идти запрещено

        if move_allowed:
            self.y: float = new_y  # Координата y героя в [м]

    def move_left(self):
        """
        Перемещает героя влево
        """

        move_allowed: bool = True  # Разрешено ли перемещаться
        speed_reduce: float = self.calculate_speed_reduce()
        speed_actual: float = self.speed_max / speed_reduce
        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_distance: float = speed_actual * time_step  # Квант перемещения в [м]
        new_x: float = self.x - delta_distance  # Предпологаемая координата x в [м] после шага
        for tree in self.game.forest.trees_list:

            # Расстояние до центра круга коллизии дерева в [м]
            distance: float = self.game.physical_engine.get_physical_distance(new_x, self.y, tree.stop_x, tree.stop_y)
            if distance <= tree.collision_radius:
                move_allowed: bool = False  # Идти запрещено
        if move_allowed:
            self.x: float = new_x  # Координата y героя в [м]

    def move_right(self):
        """
        Перемещает героя вправо
        """

        move_allowed: bool = True  # Разрешено ли перемещаться
        speed_reduce: float = self.calculate_speed_reduce()
        speed_actual: float = self.speed_max / speed_reduce
        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_distance: float = speed_actual * time_step  # Квант перемещения в [м]
        new_x: float = self.x + delta_distance  # Предпологаемая координата x в [м] после шага
        for tree in self.game.forest.trees_list:

            # Расстояние до центра круга коллизии дерева в [м]
            distance: float = self.game.physical_engine.get_physical_distance(new_x, self.y, tree.stop_x, tree.stop_y)
            if distance <= tree.collision_radius:
                move_allowed: bool = False  # Идти запрещено
        if move_allowed:
            self.x: float = new_x  # Координата y героя в [м]

    def move_up(self):
        """
        Перемещает героя вверх
        """

        move_allowed: bool = True  # Разрешено ли перемещаться
        speed_reduce: float = self.calculate_speed_reduce()
        speed_actual: float = self.speed_max / speed_reduce
        time_step: float = 1 / self.game.fps  # Квант времени в [с]
        delta_distance: float = speed_actual * time_step  # Квант перемещения в [м]
        new_y: float = self.y - delta_distance  # Предпологаемая координата y в [м] после шага
        for tree in self.game.forest.trees_list:

            # Расстояние до центра круга коллизии дерева в [м]
            distance: float = self.game.physical_engine.get_physical_distance(self.x, new_y, tree.stop_x, tree.stop_y)
            if distance <= tree.collision_radius:
                move_allowed: bool = False  # Идти запрещено

        if move_allowed:
            self.y: float = new_y  # Координата y героя в [м]

    def update_indicator_heat(self):
        """
        Обновляет значение индикатора температуры
        """

        # Физика
        t: float = self.temperature  # Температура героя в [К]

        # Температура героя в [%]
        heat_percent: float = 100 * (t - self.temperature_min) / (self.temperature_max - self.temperature_min)
        self.indicator_heat.value = heat_percent

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
        flag = False  # Показывает, движется герой в данной итерации

        for keys in self.image_hero_dict:
            button = self.game.graphic_engine.key_pressed_hero(keys)
            if button is not None:
                if self.game.tick_count - self.tick_count_start >= 13:
                    if self.key == 0:
                        self.key = 1
                    else:
                        self.key = 0
                    self.tick_count_start = self.game.tick_count

                flag = True
                image_load = self.image_hero_dict[button][self.key]
                self.game.graphic_engine.draw_image_center(image_load, x, y,
                                                           self.graphical_width, self.graphical_height)
                self.button_last = button
                self.key_last = self.key

            elif not flag:
                image_load = self.image_hero_dict[self.button_last][self.key_last]
                self.game.graphic_engine.draw_image_center(image_load, x, y,
                                                           self.graphical_width, self.graphical_height)

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
                    self.tick_count_start = self.game.tick_count

    def manage_physics(self):
        """
        Обрабатывает физические события героя
        """

        self.get_hungry()
        self.get_thirsty()
        self.check_live_parameters()
        self.update_status()
        self.update_indicator_heat()
        self.update_indicator_satiety()
        self.update_indicator_thirst()

    def process(self):
        """
        Обрабатывает события героя
        """

        self.manage_logic()
        self.manage_physics()
        self.indicator_heat.process()
        self.indicator_satiety.process()
        self.indicator_thirst.process()
