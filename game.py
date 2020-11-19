"""
Модуль игры
"""

import pygame

from forest import Forest
from hero import Hero
from logic_engine import LogicEngine


class Game(object):
    """
    Описывает игру
    """

    def __init__(self):
        """
        Параметры
        """

        # Логика
        self.actions_moment_dict: dict = {None: None}  # Словарь мгновенных действий
        self.actions_long_dict: dict = {None: None}  # Словарь продолжительных действий
        self.clock = pygame.time.Clock()  # Часы pygame
        self.status: str = 'run'  # Игра запущена

        # Графика
        self.black: tuple = (0, 0, 0)  # Чёрный цвет
        self.fps: int = 60  # Частота обновления экарана в [Гц]

        # Физика
        self.day_length: int = 600  # Длинна дня в [с]

        # Объекты
        self.forest = None  # Объект леса определяется в game.setup()
        self.hero = None  # Объект героя определяется в game.setup()
        self.logic_engine = None  # Объект логического движка определяется в game.setup()
        self.screen = None  # Определяется в game.setup()

    # --- Инициализация ---
    def setup(self):
        """
        Инициализация игры
        """

        self.set_screen()

        self.forest = Forest(self)  # Объект леса
        self.forest.setup()

        self.hero = Hero(self)  # Объект героя
        self.hero.setup()

        self.logic_engine = LogicEngine(self)  # Объект логического движка
        self.logic_engine.setup()

    # --- Логика ---
    def exit(self):
        """
        Завершает игру
        """

        self.status: str = 'exit'  # Игра завершена

    def set_screen(self):
        """
        Создаёт объект экрана
        """

        screen_height: int = 700  # Высота экрана в пикселях
        screen_width: int = 1200  # Ширина экрана в пикселях
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)  # Объект экрана pygame

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

    # --- Обработка ---
    def manage_graphics(self):
        """
        Обновляет экран
        """

        pygame.display.update()
        self.clock.tick(self.fps)
        self.screen.fill(self.black)

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

        self.logic_engine.process()
        self.manage_logic()
        self.manage_graphics()
        self.forest.process()
        self.hero.process()
