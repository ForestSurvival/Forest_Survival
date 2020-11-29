"""
Модуль деревни
"""

from pygame.draw import *


class Village(object):
    """
    Описывает деревню
    """

    def __init__(self, forest, physical_x: float, physical_y: float):
        """
        Параметры

        forest - объект леса
        physical_x - физическая координата деревни в [м]
        physical_y - физическая координата деревни в [м]
        """

        # Графика
        self.color: tuple = (39, 72, 224)  # Цвет деревни
        self.graphical_radius: int = 5  # Графический радиус деревни в [м]

        # Объекты
        self.forest = forest

        # Логика
        self.action_radius: float = 0.5  # Физический радиус действия деревни в [м]

        # Физика
        self.physical_x: float = physical_x
        self.physical_y: float = physical_y

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует деревню

        graphical_x - графическая координата x деревни в [м]
        graphical_y - графическая координата y деревни в [м]
        """

        # Объекты
        screen = self.forest.game.graphic_engine.screen  # Объект экрана Pygame

        circle(screen, self.color, (graphical_x, graphical_y), self.graphical_radius)

    # --- Логика ---
    def get_found(self):
        """
        Герой нашёл деревню
        """

        self.forest.game.status: str = 'exit'  # Игра завершена

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графичекие события деревни

        graphical_x - графическая координата x деревни в [м]
        graphical_y - графическая координата y деревни в [м]
        """

        self.draw(graphical_x, graphical_y)

    def manage_logic(self):
        """
        Обрабатывает логические события деревни
        """

        self.get_found()
