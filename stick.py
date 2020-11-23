"""
Модуль палки
"""

from pygame.draw import *


class Stick(object):
    """
    Описывает палку
    """

    def __init__(self, forest, physical_x: float, physical_y: float):
        """
        Параметры палки

        forest - объект леса
        physical_x - физическая координата x палки в [м]
        physical_y - физическая координата y палки в [м]
        """

        # Графика
        self.color: tuple = (255, 228, 205)  # Цвет палки
        self.radius: int = 5  # Радиус палки в [px]

        # Физика
        self.physical_x: float = physical_x
        self.physical_y: float = physical_y

        # Объекты
        self.forest = forest

    # --- Логика ---
    def get_collected(self):
        """
        Палка собрана героем
        """

        self.forest.game.hero.inventory.sticks_amount += 1  # Увеличить количество палок в инвентаре
        self.forest.sticks_list.remove(self)

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует палку

        graphical_x - графическая координата палки в [px]
        graphical_y - графическая координата палки в [px]
        """

        circle(self.forest.game.graphic_engine.screen, self.color, (graphical_x, graphical_y), self.radius)

    # --- Обработка ---
    def manage_logic(self):
        """
        Обрабатывает логические события палки
        """

        self.get_collected()

    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события палки

        graphical_x - графическая координата палки в [px]
        graphical_y - графическая координата палки в [px]
        """

        self.draw(graphical_x, graphical_y)
