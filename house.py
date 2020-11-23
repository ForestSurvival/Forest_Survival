"""
Класс дома
"""
import pygame
from pygame.draw import *
from random import random

from match import Match
from paper import Paper


class House(object):
    """Описывает дом"""

    def __init__(self, forest, physical_x: float, physical_y: float):
        """
        Параметры

        forest - объект леса
        physical_x - Физическая координата x дома в [м]
        physical_y - Физическая координата y дома в [м]
        """

        self.color: tuple = (41, 171, 255)  # Цвет дома
        self.graphical_height: int = 75  # Графическая высота дома в [px]
        self.graphical_width: int = 60  # Графическая ширина дома в [px]
        self.matches_amount: int = 0  # Количество спичек
        self.match_generation_chance: float = 0.999999999999999999  # Шанс нахождения спички в доме
        self.paper_amount: int = 0  # Количество листов бумаги в доме
        self.paper_generation_chance: float = 0.5  # Шанс нахождения бумаги в доме
        self.physical_x: float = physical_x
        self.physical_y: float = physical_y

        # Изображение дома в формате png
        self.picture_house = pygame.image.load('Sprites/snow_house.bmp')

        # Объекты
        self.forest = forest
        self.match = Match(self)  # Объект спички
        self.paper = Paper(self)  # Объект бумаги

    # --- Инициализация ---
    @staticmethod
    def generation_needed(generation_chance: float):
        """
        Необходима ли дальнейшая генерация

        generation_chance - шанс генерации
        """

        generation_number: float = random()
        if generation_number < generation_chance:
            return True
        else:
            return False

    def generate_matches(self):
        """
        В доме можно найти спички
        """

        while self.generation_needed(self.match_generation_chance):
            self.matches_amount += 1  # Создать спичку

    def generate_paper(self):
        """
        В доме можно найти бумагу
        """

        while self.generation_needed(self.paper_generation_chance):
            self.paper_amount += 1  # Создать бумагу

    def setup(self):
        """
        Инициализация дома
        """

        self.generate_matches()
        self.generate_paper()

    # --- Логика ---
    def collect_matches(self):
        """
        Герой забирает спички
        """

        self.forest.game.hero.inventory.matches_amount += self.matches_amount  # Герой забирает все спички
        self.matches_amount: int = 0  # Спичек не осталось

    def collect_paper(self):
        """
        Герой забирает бумагу
        """

        self.forest.game.hero.inventory.paper_amount += self.paper_amount  # Герой забирает всю бумагу
        self.paper_amount: int = 0  # Бумаги не осталось

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует дом

        graphical_x - Графическая координата x дома в [px]
        graphical_y - Графическая координата y дома в [px]
        """

        circle(self.forest.game.graphic_engine.screen, (0, 0, 0), (graphical_x, graphical_y), 10)
        graphical_x -= self.graphical_width // 2
        graphical_y -= self.graphical_height // 2

        # Вставляет изображение дома
        self.forest.game.graphic_engine.screen.blit(self.picture_house, (graphical_x, graphical_y))

    def transform(self):
        """
        Изменяет размер изображения
        """

        self.picture_house = pygame.transform.scale(self.picture_house, (self.graphical_height, self.graphical_width))

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события дома

        graphical_x - Графическая координата x дома в [px]
        graphical_y - Графическая координата y дома в [px]
        """

        self.transform()
        self.draw(graphical_x, graphical_y)

    def manage_logic(self):
        """
        Обрабатывает логические события дома
        """

        self.collect_matches()
        self.collect_paper()
