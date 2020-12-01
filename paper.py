"""
Модуль бумаги
"""

import pygame


class Paper(object):
    """
    Описывает бумагу
    """

    def __init__(self, house):
        """
        Параметры

        forest - объект дома
        """

        # Графика
        self.graphical_height: int = 20  # Графическая высота бумаги в [px]
        self.graphical_width: int = 20  # Графическая ширина бумаги в [px]

        # Изображение палки в формате bmp
        self.image_paper = pygame.image.load('Sprites/paper.bmp')

        # Объекты
        self.house = house

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует бумагу

        graphical_x - Графическая координата x бумаги в [px]
        graphical_y - Графическая координата y бумаги в [px]
        """

        self.house.forest.game.graphic_engine.draw_image(self.image_paper, graphical_x, graphical_y, self.graphical_width,
                                                   self.graphical_height)

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события бумаги

        graphical_x - Графическая координата x бумаги в [px]
        graphical_y - Графическая координата y бумаги в [px]
        """

        self.draw(graphical_x, graphical_y)
