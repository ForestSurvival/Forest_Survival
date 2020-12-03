"""
Модуль леса
"""

import math

from pygame.draw import *
from random import *

from apple import Apple
from house import House
from tree import Tree
from village import Village
from stick import Stick


class Forest(object):
    """
    Описывает лес
    """

    def __init__(self, game):
        """
        Параметры

        game - объект игры
        """

        # Логика
        self.logical_dict: dict = {None: None}  # Логический словарь определяется в forest.setup()

        # Физика
        self.borders_dict = None  # Словари границ определяется в forest.setup()

        # Расстояние между границами леса по горизонтали в [м] определяется в forest.setup()
        self.borders_distance_x = None

        # Расстояние между границами леса по вертикали в [м] определяется в forest.setup()
        self.borders_distance_y = None

        self.draw_distance_max = None  # Максимальное расстояние прорисовки в [м] определяется в forest.setup()
        self.scale: int = 35  # Масштаб в [px/м]

        # Объекты
        self.apples_list: list = []  # Список яблок
        self.campfires_list: list = []  # Список костров
        self.game = game
        self.houses_list: list = []  # Список домов
        self.trees_list: list = []  # Список деревьев
        self.villages_list: list = []  # Список деревень
        self.sticks_list: list = []  # Список палок

        # Графика

        # Изображение фона в формате png
        # self.game_background = pygame.image.load('Sprites/game_background.png')

        self.border_color: tuple = (185, 250, 250)  # Цвет границ
        self.border_width: int = 1  # Толщина границ в [px]
        self.color: tuple = (193, 86, 217)  # Цвет леса
        self.graphical_dict: dict = {'walk': [self.draw_borders,
                                              self.draw_trees,
                                              self.draw_apples,
                                              self.draw_campfires,
                                              self.draw_houses,
                                              self.draw_villages,
                                              self.draw_sticks],
                                     'act': [self.draw_borders,
                                             self.draw_trees,
                                             self.draw_apples,
                                             self.draw_campfires,
                                             self.draw_houses,
                                             self.draw_villages,
                                             self.draw_sticks],
                                     'crafts': [None],
                                     'inventory': [None]}

    # --- Инициализация ---
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
        self.borders_distance_x: float = x_right - x_left  # Расстояние между границами вдоль оси x в [м]
        self.borders_distance_y: float = y_down - y_up  # Расстояние между границами по y в [м]

    def count_draw_distance(self):
        """
        Вычисляет расстояние прорисовки в [м]
        """

        screen_height: int = self.game.graphic_engine.screen.get_height()  # Высота экрана в [px]
        screen_width: int = self.game.graphic_engine.screen.get_width()  # Ширина экрана в [px]

        # Максимальное расстояние на экране в [px]
        max_screen_distance: float = math.sqrt(screen_height ** 2 + screen_width ** 2)

        max_distance: float = max_screen_distance / self.scale  # Максимальное расстояние до видимого объекта в [м]
        self.draw_distance_max: int = math.ceil(max_distance)  # Максимальное расстояние прорисовки в []

    def create_borders(self):
        """
        Создаёт словарь границ
        """

        down_border_dict: dict = {'coordinate': 'y',
                                  'value': 20}  # Словарь нижней границы леса
        left_border_dict: dict = {'coordinate': 'x',
                                  'value': -20}  # Словаь левой границы леса
        right_border_dict: dict = {'coordinate': 'x',
                                   'value': 20}  # Словарь правой границы леса
        up_border_dict: dict = {'coordinate': 'y',
                                'value': -20}  # Словарь верхней границы леса
        self.borders_dict: dict = {'down': down_border_dict,  # Словарь границ
                                   'left': left_border_dict,
                                   'right': right_border_dict,
                                   'up': up_border_dict}

    def generate_apples(self):
        """
        Создаёт яблоки
        """

        apples_amount: int = 10  # Количество яблок
        for apple_number in range(apples_amount):

            # Координата x яблока в [м]
            x_apple: float = random() * self.borders_distance_x + self.borders_dict['left']['value']

            # Координата y яблока в [м]
            y_apple: float = random() * self.borders_distance_y + self.borders_dict['up']['value']

            apple = Apple(self, x_apple, y_apple)  # Объект яблока
            self.apples_list.append(apple)

    def generate_houses(self):
        """
        Создаёт дома
        """

        # Физика
        houses_amount: int = 3  # Количество домов
        distance_min: float = 5  # Минимальное расстояние между домами в [м]

        for house_number in range(houses_amount):

            generated_too_close: bool = False  # Флаг слишком близкой генерации домов

            # Физическая координата x дома в [м]
            house_x: float = random() * self.borders_distance_x + self.borders_dict['left']['value']

            # Физическая координата y дома в [м]
            house_y: float = random() * self.borders_distance_y + self.borders_dict['up']['value']
            for other in self.houses_list:
                distance: float = self.game.physical_engine.get_physical_distance(house_x, house_y, other.physical_x,
                                                                                  other.physical_y)
                if distance < distance_min:  # Если дома сгенерировались слишком близко
                    generated_too_close: bool = True  # Запомнить это
            if not generated_too_close:  # Если дома не очень близко
                house = House(self, house_x, house_y)  # Объект яблока
                house.setup()
                self.houses_list.append(house)

    def generate_trees(self):
        """
        Создаёт деревья
        """

        trees_amount: int = 100  # Количество деревьев
        for tree_number in range(trees_amount):
            # Физическая координата x дерева в [м]
            tree_physical_x: float = random() * self.borders_distance_x + self.borders_dict['left']['value']

            # Физическая координата y дерева в [м]
            tree_physical_y: float = random() * self.borders_distance_y + self.borders_dict['up']['value']

            tree = Tree(self, tree_physical_x, tree_physical_y)  # Объект дерева
            self.trees_list.append(tree)

    def generate_villages(self):
        """
        Создаёт деревни
        """

        villages_amount: int = 1  # Количество деревень
        for village_number in range(villages_amount):
            # Физическая координата x деревни в [м]
            village_physical_x: float = random() * self.borders_distance_x + self.borders_dict['left']['value']

            # Физическая координата y деревни в [м]
            village_physical_y: float = random() * self.borders_distance_y + self.borders_dict['up']['value']

            village = Village(self, village_physical_x, village_physical_y)  # Объект деревни
            self.villages_list.append(village)

    def generate_sticks(self):
        """
        Создаёт палки
        """

        sticks_amount: int = 20  # Количество палок
        for stick_number in range(sticks_amount):
            # Координата x палки в [м]
            stick_x: float = random() * self.borders_distance_x + self.borders_dict['left']['value']

            # Координата y палки в [м]
            stick_y: float = random() * self.borders_distance_y + self.borders_dict['up']['value']

            stick = Stick(self, stick_x, stick_y)  # Объект палки
            self.sticks_list.append(stick)

    def set_logical_dict(self):
        """
        Создаёт словарь, сопоставляющий статус героя и действия окружающей среды
        """
        self.logical_dict: dict = {'walk': [None],  # Логический действий
                                   'act': [self.manage_apples_logic,
                                           self.manage_campfires_logic,
                                           self.manage_houses_logic,
                                           self.manage_villages_logic,
                                           self.manage_sticks_logic],
                                   'crafts': [self.game.hero.inventory.process],
                                   'inventory': [self.game.hero.inventory.process],
                                   'exit': [None]}

    def setup(self):
        """
        Действия при создании леса
        """

        self.set_logical_dict()
        self.create_borders()
        self.count_max_distance()
        self.count_draw_distance()
        self.generate_apples()
        self.generate_houses()
        self.generate_trees()
        self.generate_villages()
        self.generate_sticks()

    # --- Логика ---
    def convert_horizontal_m_to_px(self, coordinate_m: float):
        """
        Преобразует [м] в [px] по горизонтали

        coordinate_m - координата объекта в [м]
        """

        distance_m: float = coordinate_m - self.game.hero.x  # Расстояние от героя до объекта в [м]
        distance_raw: float = distance_m * self.scale  # Расстояние в [px]
        distance_px: int = round(distance_raw)  # Округлённое расстояние в [px]

        # Координата  объекта в [px]
        distance_px_cooked: int = distance_px + self.game.graphic_engine.screen.get_width() // 2

        return distance_px_cooked

    def convert_vertical_m_to_px(self, coordinate_m: float):
        """
        Преобразует [м] в [px] по вертикали

        coordinate_m - координата объекта в [м]
        """

        distance_m: float = coordinate_m - self.game.hero.y  # Расстояние от героя до объекта в [м]
        distance_raw: float = distance_m * self.scale  # Расстояние в [px]
        distance_px: int = round(distance_raw)  # Округлённое расстояние в [px]

        # Координата  объекта в [px]
        distance_px_cooked: int = distance_px + self.game.graphic_engine.screen.get_height() // 2

        return distance_px_cooked

    def manage_apples_logic(self):
        """
        Обрабатывает действия героя над яблоками
        """

        # Движки
        physical_engine = self.game.physical_engine

        # Объекты
        close_apple = physical_engine.find_close_object(self.apples_list)  # Близкое к герою яблоко

        if close_apple is not None:  # Если существует близкое к герою яблоко
            close_apple.manage_logic()

    def manage_campfires_logic(self):
        """
        Обрабатывает действия героя над кострами
        """

        # Движки
        physical_engine = self.game.physical_engine

        # Объекты
        close_campfire = physical_engine.find_close_object(self.campfires_list)  # Близкий к герою костёр

        if close_campfire is not None:  # Если рядом с героем есть костёр
            close_campfire.manage_logic()

    def manage_houses_logic(self):
        """
        Обрабатывает действия героя над домами
        """

        for house in self.houses_list:

            # Список компонент физического расстояния до дома в [м]
            distance_list: list = self.calculate_distance_to_point(house.physical_x, house.physical_y)

            # Физическое расстояние до дома в [м]
            distance: float = math.sqrt(distance_list[0] ** 2 + distance_list[1] ** 2)

            if distance <= self.game.hero.action_radius:
                house.manage_logic()

    def manage_villages_logic(self):
        """
        Обрабатывает действия героя над деревнями
        """

        # Движки
        physical_engine = self.game.physical_engine

        # Объекты
        close_village = physical_engine.find_close_object(self.villages_list)  # Близкая к герою деревня

        if close_village is not None:  # Если существует близкая к герою деревня
            close_village.manage_logic()

    def manage_sticks_logic(self):
        """
        Обрабатывает действия героя над палками
        """

        for stick in self.sticks_list:

            # Список компонент физического расстояния до палки в [м]
            distance_list: list = self.calculate_distance_to_point(stick.physical_x, stick.physical_y)

            # Физическое расстояние до палки в [м]
            distance: float = math.sqrt(distance_list[0] ** 2 + distance_list[1] ** 2)

            if distance <= self.game.hero.action_radius:
                stick.manage_logic()

    # --- Физика ---
    def calculate_distance_to_line(self, line_dict: dict):
        """
        Вычисляет расстояние от героя до прямой

        line_dict - словарь прямой
        """

        coordinate_dict: dict = {'x': self.game.hero.x,  # Словарь координат
                                 'y': self.game.hero.y}
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

        x_distance: float = x - self.game.hero.x  # Расстояние от героя до точки вдоль оси x в [м]
        y_distance: float = y - self.game.hero.y  # Расстояние от героя до точки вдоль оси y в [м]
        distance_list: list = [x_distance, y_distance]  # Компоненты расстояния от героя до точки в [м]
        return distance_list

    def draw_needed(self, distance: float):
        """
        Проверяет, нужно ли рисовать объект

        line_dict - словарь прямой
        """

        if distance <= self.draw_distance_max:  # Если прямую надо прорисовывать
            return True
        else:
            return False

    # --- Графика ---
    def draw_apples(self):
        """
        Рисует яблоки
        """

        for apple in self.apples_list:

            # Физическое расстояние до яблока в [м]
            distance_x: float = apple.physical_x - self.game.hero.x
            distance_y: float = apple.physical_y - self.game.hero.y
            apple_physical_distance: float = math.sqrt(distance_x ** 2 + distance_y ** 2)

            if self.draw_needed(apple_physical_distance):

                # Графическая координата x яблока в [px]
                apple_graphical_x: int = self.convert_horizontal_m_to_px(apple.physical_x)

                # Графическая координата y яблока в [px]
                apple_graphical_y: int = self.convert_vertical_m_to_px(apple.physical_y)

                apple.manage_graphics(apple_graphical_x, apple_graphical_y)

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
        y_2: int = self.game.graphic_engine.screen.get_height() + 1  # Нижняя точка ниже экрана
        screen = self.game.graphic_engine.screen

        line(screen, self.border_color, [line_coordinate, y_1], [line_coordinate, y_2], self.border_width)

    def draw_campfires(self):
        """
        Рисует костры
        """

        for campfire in self.campfires_list:
            # Графическая координата x дома в [px]
            campfire_graphical_x: int = self.convert_horizontal_m_to_px(campfire.physical_x)

            # Графическая координата y дома в [px]
            campfire_graphical_y: int = self.convert_vertical_m_to_px(campfire.physical_y)

            campfire.manage_graphics(campfire_graphical_x, campfire_graphical_y)

    def draw_houses(self):
        """
        Рисует дома
        """

        for house in self.houses_list:

            # Физическое расстояние до дома в [м]
            distance_x: float = house.physical_x - self.game.hero.x
            distance_y: float = house.physical_y - self.game.hero.y
            house_physical_distance: float = math.sqrt(distance_x ** 2 + distance_y ** 2)

            if self.draw_needed(house_physical_distance):

                # Графическая координата x дома в [px]
                house_graphical_x: int = self.convert_horizontal_m_to_px(house.physical_x)

                # Графическая координата y дома в [px]
                house_graphical_y: int = self.convert_vertical_m_to_px(house.physical_y)

                house.manage_graphics(house_graphical_x, house_graphical_y)

    def draw_trees(self):
        """
        Рисует деревья
        """

        for tree in self.trees_list:

            # Физическое расстояние до дерева в [м]
            distance_x: float = tree.physical_x - self.game.hero.x
            distance_y: float = tree.physical_y - self.game.hero.y
            tree_physical_distance: float = math.sqrt(distance_x ** 2 + distance_y ** 2)

            if self.draw_needed(tree_physical_distance):

                # Графическая координата x дома в [px]
                tree_graphical_x: int = self.convert_horizontal_m_to_px(tree.physical_x)

                # Графическая координата y дома в [px]
                tree_graphical_y: int = self.convert_vertical_m_to_px(tree.physical_y)

                tree.manage_graphics(tree_graphical_x, tree_graphical_y)

    def draw_villages(self):
        """
        Рисует деревни
        """

        for village in self.villages_list:

            # Физическое расстояние до деревни в [м]
            distance_x: float = village.physical_x - self.game.hero.x
            distance_y: float = village.physical_y - self.game.hero.y
            village_physical_distance: float = math.sqrt(distance_x ** 2 + distance_y ** 2)

            if self.draw_needed(village_physical_distance):

                # Графическая координата x деревни в [px]
                village_graphical_x: int = self.convert_horizontal_m_to_px(village.physical_x)

                # Графическая координата y деревни в [px]
                village_graphical_y: int = self.convert_vertical_m_to_px(village.physical_y)

                village.manage_graphics(village_graphical_x, village_graphical_y)

    def draw_vertical_line(self, line_coordinate: float):
        """
        Рисует вертикальную прямую

        line_coordinate - Координата прямой в [м]
        """

        x_1: int = -1  # Левая точка левее экрана
        x_2: int = self.game.graphic_engine.screen.get_width() + 1  # Правая точка правее экрана

        screen = self.game.graphic_engine.screen
        line(screen, self.border_color, [x_1, line_coordinate], [x_2, line_coordinate], self.border_width)

    def draw_sticks(self):
        """
        Рисует палки
        """

        for stick in self.sticks_list:

            # Физическое расстояние до палки в [м]
            distance_x: float = stick.physical_x - self.game.hero.x
            distance_y: float = stick.physical_y - self.game.hero.y
            stick_physical_distance: float = math.sqrt(distance_x ** 2 + distance_y ** 2)

            if self.draw_needed(stick_physical_distance):

                # Графическая координата x палки в [px]
                stick_graphical_x: int = self.convert_horizontal_m_to_px(stick.physical_x)

                # Графическая координата y палки в [px]
                stick_graphical_y: int = self.convert_vertical_m_to_px(stick.physical_y)

                stick.manage_graphics(stick_graphical_x, stick_graphical_y)

    # --- Обработка ---
    def manage_logic(self):
        """
        Обрабатывает логические события леса
        """

        logical_list: list = self.logical_dict[self.game.hero.status_current]  # Список действий
        for logical_action in logical_list:
            if logical_action is not None:
                logical_action()

    def manage_graphics(self):
        """
        Обрабатывает графические события леса
        """

        graphical_list: list = self.graphical_dict[self.game.hero.status_current]
        for graphical_action in graphical_list:
            if graphical_action is not None:
                graphical_action()

    def process(self):
        """
        Обрабатывает события леса
        """

        self.manage_logic()
        self.manage_graphics()
        self.process_campfires()

    def process_campfires(self):
        """
        Обрабатывает события костров
        """

        for campfire in self.campfires_list:
            campfire.process()
