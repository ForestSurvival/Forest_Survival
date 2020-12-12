"""
Модуль воды
"""

import pygame


class Water(object):
    """
    Описывает воду
    """

    def __init__(self, inventory):
        """
        Параметры

        inventory - объект инвнтаря
        """

        # Графика
        self.graphical_height: int = 25  # Графическая высота воды в [px]
        self.graphical_width: int = 25  # Графическая ширина воды в [px]

        # Изображение палки в формате bmp
        self.image_water = pygame.image.load('Sprites/water.bmp')

        # Физика
        self.volume = 0.001  # Объём в [м^3]

        # Объекты
        self.inventory = inventory

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует воду

        graphical_x - графическая координата x воды в [px]
        graphical_y - графическая координата y воды в [px]
        """

        self.inventory.hero.game.graphic_engine.draw_image_center(self.image_water, graphical_x, graphical_y,
                                                                  self.graphical_width, self.graphical_height)

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события спички

        graphical_x - Графическая координата x спички в [px]
        graphical_y - Графическая координата y спички в [px]
        """

        self.draw(graphical_x, graphical_y)
