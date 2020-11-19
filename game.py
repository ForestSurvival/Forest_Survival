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

    def __init__(self, screen):
        """
        Параметры

        screen - экран pygame
        """

        # Логика
        self.actions_moment_dict: dict = {None: None}  # Словарь мгновенных действий
        self.actions_long_dict: dict = {None: None}  # Словарь продолжительных действий
        self.clock = pygame.time.Clock()  # Часы pygame
        self.status: str = 'run'  # Игра запущена

        # Графика
        self.black: tuple = (0, 0, 0)  # Чёрный цвет
        self.fps: int = 60  # Частота обновления экарана в [Гц]
        self.screen = screen

        # Физика
        self.day_length: int = 600  # Длинна дня в [с]
        self.time_step: float = 1 / self.fps  # Квант времени в [с]

        # Объекты
        self.forest = None  # Объект леса определяется в game.setup()
        self.graphic_engine = None  # Объект крафического движка определяется в game.setup()
        self.hero = None  # Объект героя определяется в game.setup()
        self.logic_engine = None  # Объект логического движка определяется в game.setup()

    # --- Инициализация ---
    def setup(self):
        """
        Инициализация игры
        """

        self.forest = Forest(self)  # Объект леса
        self.hero = Hero(self)  # Объект героя
        self.logic_engine = LogicEngine(self)  # Объект логического движка
        self.forest.setup()
        self.hero.setup()
        self.logic_engine.setup()

    # --- Логика ---
    def finish(self):
        """
        Завершает игру
        """

        self.status: str = 'exit'  # Игра завершена

    def manage_logic(self):
        """
        Обрабатывает логические события
        """

        self.update_actions_dicts()
        for key_index in range(self.logic_engine.keys_amount):
            if key_index in self.actions_moment_dict:
                if self.logic_engine.keys_moment_list[key_index] == 1:  # Если кнопка нажата строго в текущем цикле
                    self.actions_moment_dict[key_index]()

    def update_actions_dicts(self):
        """
        Создаёт словарь действий
        """

        if self.hero.status_current == 'walk':  # Если герой может перемещаться
            self.actions_moment_dict: dict = {pygame.K_ESCAPE: self.finish}  # Словарь мгновенных действий
            self.actions_long_dict: dict = {None: None}  # Словарь продолжительных действий
        elif self.hero.status_current == 'inventory':  # Если герой просматривает инвентарь
            self.actions_moment_dict: dict = {None: None}  # Словарь мгновенных действий
            self.actions_long_dict: dict = {None: None}  # Словарь продолжительных действий
        else:
            self.actions_moment_dict: dict = {None: None}  # Словарь мгновенных действий
            self.actions_long_dict: dict = {None: None}  # Словарь продолжительных действий

    def switch_to_main_status(self):
        """
        Перевелит игру в основное состояние
        """

        self.status: str = 'main'  # Основное состояние игры

    # --- Графика ---
    def manage_graphics(self):
        """
        Обновляет экран
        """

        pygame.display.update()
        self.clock.tick(self.fps)
        self.screen.fill(self.black)

    # --- Обработка ---
    def process(self):
        """
        Обрабатывает события игры
        """

        self.manage_graphics()
        self.logic_engine.process()
        self.hero.process()
