"""
Модуль яблока
"""

import pygame


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

        # Графика
        self.graphical_height: int = 25  # Графическая высота яблока в [px]
        self.graphical_width: int = 25  # Графическая ширина яблока в [px]

        # Изображение палки в формате bmp
        self.image_apple = pygame.image.load('Sprites/apple.bmp')

        # Объекты
        self.forest = forest

        # Физика
        self.satiety: float = 196.7796  # Пищевая энергетическая ценность яблока в [Дж]
        self.physical_x: float = physical_x
        self.physical_y: float = physical_y

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

        self.forest.game.graphic_engine.draw_image_center(self.image_apple, graphical_x, graphical_y, self.graphical_width,
                                                          self.graphical_height)

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
