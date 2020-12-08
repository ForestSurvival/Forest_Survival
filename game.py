"""
Модуль игры
"""

import pygame

from forest import Forest
from hero import Hero
from graphic_engine import GraphicEngine
from logic_engine import LogicEngine
from menu import Menu
from physical_engine import PhysicalEngine


class Game(object):
    """
    Описывает игру
    """

    def __init__(self):
        """
        Параметры
        """

        # Движки
        self.graphic_engine = None  # Объект графического движка определяется в game.setup()
        self.logic_engine = None  # Объект логического движка определяется в game.setup()
        self.physical_engine = None  # Объект физического движка определяется в game.setup()

        # Логика
        self.actions_moment_dict: dict = {None: None}  # Словарь мгновенных действий
        self.actions_long_dict: dict = {None: None}  # Словарь продолжительных действий
        self.clock = pygame.time.Clock()  # Часы pygame
        self.status: str = 'menu'  # Игра находится в меню

        # Графика
        self.black: tuple = (0, 0, 0)  # Чёрный цвет
        self.fps: int = 60  # Частота обновления экарана в [Гц]

        # Физика
        self.day_length: int = 600  # Длинна дня в [с]
        self.tick_count: int = 0  # Количесто циклов, прошедших с начала игры

        # Объекты
        self.forest = None  # Объект леса определяется в game.setup()
        self.hero = None  # Объект героя определяется в game.setup()
        self.menu = Menu(self)  # Объект меню

    # --- Инициализация ---
    def setup(self):
        """
        Инициализация игры
        """

        # Движки
        self.graphic_engine = GraphicEngine(self)  # Объект графического движка
        self.graphic_engine.setup()
        self.logic_engine = LogicEngine(self)  # Объект логического движка
        self.logic_engine.setup()
        self.physical_engine = PhysicalEngine(self)  # Объект физческого движка

        # Объекты
        self.hero = Hero(self)  # Объект героя
        self.forest = Forest(self)  # Объект леса

        self.forest.setup()

        self.hero.setup()
        self.menu.setup()

    # --- Логика ---
    def exit(self):
        """
        Завершает игру
        """

        if self.status == 'run':  # Если игра запущена
            self.status: str = 'menu'  # Выйти в меню
        elif self.status == 'menu':  # Если открыто меню
            self.status: str = 'exit'  # Выйти из игры

    def play(self):
        """
        Запускает игру
        """

        self.status: str = 'run'  # Игра запущена
          
    def update_actions_dicts(self):
        """
        Создаёт словарь действий
        """

        if self.hero.status_current == 'walk':  # Если герой может перемещаться
            self.actions_moment_dict: dict = {pygame.K_ESCAPE: self.exit}  # Словарь мгновенных действий
            self.actions_long_dict: dict = {None: None}  # Словарь продолжительных действий
        else:
            self.actions_moment_dict: dict = {None: None}  # Словарь мгновенных действий
            self.actions_long_dict: dict = {None: None}  # Словарь продолжительных действий

    # --- Физика ---
    def increase_tick_count(self):
        """
        Увеличивает кол-во циклов
        """

        self.tick_count += 1

    # --- Обработка ---
    def manage_graphics(self):
        """
        Обновляет экран
        """

        pygame.display.update()
        self.clock.tick(self.fps)
        self.graphic_engine.screen.fill((255, 255, 255))

    def manage_logic(self):
        """
        Обрабатывает логические события
        """

        self.update_actions_dicts()
        for key_index in range(self.logic_engine.keys_amount):
            if key_index in self.actions_moment_dict:
                if self.logic_engine.keys_moment_list[key_index] == 1:  # Если кнопка нажата строго в текущем цикле
                    self.actions_moment_dict[key_index]()

    def process(self):
        """
        Обрабатывает события игры
        """

        self.increase_tick_count()
        self.logic_engine.process()
        self.manage_graphics()
        self.manage_logic()
        if self.status == 'menu':
            self.menu.manage_graphics()
            self.menu.manage_logic()
        elif self.status == 'run':
            self.physical_engine.manage_physics()
            self.forest.process()
            self.hero.process()
