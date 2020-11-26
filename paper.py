"""
Модуль бумаги
"""

from pygame.draw import *


class Paper(object):
    """
    Описывает бумагу
    """

    def __init__(self, house):
        """
        Параметры

        forest - объект дома
        """

        self.color: tuple = (16, 77, 57)  # Цвет бумаги
        self.graphical_radius: int = 5  # Радиус бумаги в [px]

        # Объекты
        self.house = house

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует бумагу

        graphical_x - Графическая координата x бумаги в [px]
        graphical_y - Графическая координата y бумаги в [px]
        """

        circle(self.house.forest.game.graphic_engine.screen, self.color, (graphical_x, graphical_y), self.graphical_radius)

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события бумаги

        graphical_x - Графическая координата x бумаги в [px]
        graphical_y - Графическая координата y бумаги в [px]
        """

        self.draw(graphical_x, graphical_y)
