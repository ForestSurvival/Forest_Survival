"""
Модуль воды
"""

from pygame.draw import *


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
        self.color: tuple = (221, 242, 50)  # Цвет воды
        self.graphical_radius: int = 5  # Графический радиус воды в [px]

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

        # Объекты
        screen = self.inventory.hero.game.graphic_engine.screen  # Объект экрана Pygame

        circle(screen, self.color, (graphical_x, graphical_y), self.graphical_radius)
