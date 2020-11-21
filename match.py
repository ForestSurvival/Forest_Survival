"""
Модуль спички
"""

from pygame.draw import *


class Match(object):
    """
    Описывает спичку
    """

    def __init__(self, house):
        """
        Параметры

        forest - объект дома
        """

        self.color: tuple = (176, 254, 177)  # Цвет спички
        self.radius: int = 5  # Радиус спички в [px]

        # Объекты
        self.house = house

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует бумагу

        graphical_x - Графическая координата x спички в [px]
        graphical_y - Графическая координата y спички в [px]
        """

        circle(self.house.forest.game.screen, self.color, (graphical_x, graphical_y), self.radius)

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события спички

        graphical_x - Графическая координата x спички в [px]
        graphical_y - Графическая координата y спички в [px]
        """

        self.draw(graphical_x, graphical_y)
