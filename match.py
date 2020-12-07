"""
Модуль спички
"""

import pygame


class Match(object):
    """
    Описывает спичку
    """

    def __init__(self, house):
        """
        Параметры

        forest - объект дома
        """

        # Графика
        self.graphical_height: int = 20  # Графическая высота спички в [px]
        self.graphical_width: int = 20  # Графическая ширина спички в [px]

        # Изображение палки в формате bmp
        self.image_match = pygame.image.load('Sprites/match.bmp')

        # Объекты
        self.house = house

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует бумагу

        graphical_x - Графическая координата x спички в [px]
        graphical_y - Графическая координата y спички в [px]
        """

        self.house.forest.game.graphic_engine.draw_image_center(self.image_match, graphical_x, graphical_y, self.graphical_width,
                                                                self.graphical_height)

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события спички

        graphical_x - Графическая координата x спички в [px]
        graphical_y - Графическая координата y спички в [px]
        """

        self.draw(graphical_x, graphical_y)
