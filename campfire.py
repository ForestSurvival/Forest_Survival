"""
Модуль костра
"""

from pygame.draw import *


class Campfire(object):
    """
    Описывает костёр
    """

    def __init__(self, inventory, physical_x: float, physical_y: float):
        """
        Параметры

        inventory - объект инвентаря
        physical_x - физическая координата x костра в [м]
        physical_y - физическая координата y костра в [м]
        """

        # Физика
        self.physical_x: float = physical_x
        self.physical_y: float = physical_y
        self.matches_amount: int = 1  # Необходимое количество спичек
        self.paper_amount: int = 1  # Необходимое колчество бумаги
        self.sticks_amount: int = 5  # Необходимое количество палок

        # Графика
        self.color: tuple = (128, 0, 0)  # Цвет костра
        self.graphical_radius: int = 5  # Графический радиус костра в [px]

        # Объекты
        self.inventory = inventory  # Объект инвентаря

    # --- Логика ---
    def get_created(self):
        """
        Герой создаёт костёр
        """

        self.inventory.hero.game.forest.campfires_list.append(self)

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует костёр

        graphical_x - графическая координата x костра в [px]
        graphical_y - графическая координата y костра в [px]
        """

        # Объекты
        screen = self.inventory.hero.game.graphic_engine.screen  # Объект экрана Pygame

        circle(screen, self.color, (graphical_x, graphical_y), self.graphical_radius)

    # --- Физика ---
    def melt_snow(self):
        """
        Растопить снег
        """

        self.inventory.water_amount += 1  # Добавить воду в инвентарь

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события костра

        graphical_x - графическая координата x костра в [px]
        graphical_y - графическая координата y костра в [px]
        """

        self.draw(graphical_x, graphical_y)

    def manage_logic(self):
        """
        Обрабатывает логические события костра
        """

        self.melt_snow()
