"""
Модуль яблока
"""

from pygame.draw import *


class Apple(object):
    """
    Описывает яблоко
    """

    def __init__(self, screen, x: float, y: float):
        """
        Параметры

        Координаты центра яблока

        x - координата x яблока в [м]
        y - координата y яблока в [м]
        screen - экран pygame
        """

        self.color: tuple = (5, 95, 23)  # Цвет яблока
        self.radius: int = 5  # Радиус яблока в [px]
        self.screen = screen
        self.x: float = x
        self.y: float = y

    # --- Логика ---
    @staticmethod
    def process_action():
        """
        Описывает взаимодействие героя и яблака
        """

        print('Action')

    # --- Графика ---
    def draw(self, x: int, y: int):
        """
        Рисует яблоко

        x - координата яблока в [px]
        y - координата яблока в [px]
        """

        circle(self.screen, self.color, (x, y), self.radius)
