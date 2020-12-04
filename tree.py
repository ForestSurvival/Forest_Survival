"""
Модуль дерева
"""

from pygame.draw import *


class Tree(object):
    """
    Описывает дерево
    """

    def __init__(self, forest, physical_x: float, physical_y: float):
        """
        Параметры

        forest - объект леса
        physical_x - физическая координата x дерева в [м]
        physical_y - физическая координата y дерева в [м]
        """

        # Графика
        self.color: tuple = (255, 163, 136)  # Цвет дерева
        self.graphical_radius: int = 5  # Графический радиус дерева в [px]

        # Объекты
        self.forest = forest

        # Физика
        self.physical_x: float = physical_x
        self.physical_y: float = physical_y

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует дерево

        graphical_x - графическая координата x дерева в px]
        graphical_y - графическая координата y дерева в [px]
        """

        circle(self.forest.game.graphic_engine.screen, self.color, (graphical_x, graphical_y), self.graphical_radius)

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события дерева

        graphical_x - графическая координата x дерева в px]
        graphical_y - графическая координата y дерева в [px]
        """

        self.draw(graphical_x, graphical_y)
