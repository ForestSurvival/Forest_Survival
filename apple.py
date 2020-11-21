"""
Модуль яблока
"""

from pygame.draw import *


class Apple(object):
    """
    Описывает яблоко
    """

    def __init__(self, forest, physical_x: float, physical_y: float):
        """
        Параметры

        forest - объект леса
        physical_x - Физическая координата x яблока в [м]
        physical_y - Физическая координата y яблока в [м]
        """

        self.color: tuple = (5, 95, 23)  # Цвет яблока
        self.radius: int = 5  # Радиус яблока в [px]
        self.satiety: float = 196.7796  # Пищевая энергетическая ценность яблока в [Дж]
        self.physical_x: float = physical_x
        self.physical_y: float = physical_y

        # Объекты
        self.forest = forest

    # --- Логика ---
    def get_collected(self):
        """
        Яблоко собрано героем
        """

        self.forest.game.hero.inventory.apples_amount += 1  # Добавить яблоко в инвентарь героя
        self.forest.apples_list.remove(self)

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует яблоко

        graphical_x - Графическая координата x яблока в [px]
        graphical_y - Графическая координата y яблока в [px]
        """

        circle(self.forest.game.screen, self.color, (graphical_x, graphical_y), self.radius)

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события яблока

        graphical_x - Графическая координата x яблока в [px]
        graphical_y - Графическая координата y яблока в [px]
        """

        self.draw(graphical_x, graphical_y)

    def manage_logic(self):
        """
        Обрабатывает логические события яблока
        """

        self.get_collected()
