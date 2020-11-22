"""
Модуль костра
"""

from pygame.draw import *


class Campfire(object):
    """
    Описывает костёр
    """

    def __init__(self, crafts, physical_x: float, physical_y: float):
        """
        Параметры

        crafts - объект крафтов
        physical_x - физическая координата x костра в [м]
        physical_y - физическая координата y костра в [м]
        """

        # Физика
        self.physical_x: float = physical_x
        self.physical_y: float = physical_y

        # Графика
        self.color: tuple = (0, 0, 0)  # Цвет костра
        self.graphical_radius: int = 5  # Графический радиус костра в [px]

        # Объекты
        self.crafts = crafts

    # --- Логика ---
    def get_created(self):
        """
        Герой создаёт костёр
        """

        self.crafts.hero.game.forest.campfires_list.append(self)

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует костёр

        graphical_x - графическая координата x костра в [px]
        graphical_y - графическая координата y костра в [px]
        """

        circle(self.crafts.hero.game.screen, self.color, (graphical_x, graphical_y), self.graphical_radius)

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события костра

        graphical_x - графическая координата x костра в [px]
        graphical_y - графическая координата y костра в [px]
        """

        self.draw(graphical_x, graphical_y)
