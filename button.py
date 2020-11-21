"""
Модуль кнопки
"""

from pygame.draw import *


class Button(object):
    """
    Описывает кнопку
    """

    def __init__(self, function, inventory, graphical_x: int, graphical_y: int):
        """
        Параметры

        function - функция кнопки
        inventory - объект инвентаря
        graphical_x - графическая координата x копки в [px]
        graphical_y - графическая координата y кнопки в [px]
        """

        # Логика
        self.function = function

        # Физика
        self.height: int = 30  # Высота кнопки в [px]
        self.width: int = 100  # Ширина кнопки в [px]
        self.graphical_x: int = graphical_x
        self.graphical_y: int = graphical_y

        # Объекты
        self.inventory = inventory

        # Графика
        self.color: tuple = (203, 247, 72)  # Цвет кнопки

    # --- Логика ---
    def manage_click(self):
        """
        Обрабатывает нажатие
        """

        mouse_pos: list = self.inventory.hero.game.logic_engine.mouse_pos_list  # Список координат мыши
        if mouse_pos != [None]:  # Если кнопка мыши нажата
            mouse_x: int = mouse_pos[0]  # Координата x мыши в [px]
            mouse_y: int = mouse_pos[1]  # Координата y мыши в [px]
            if self.graphical_x <= mouse_x <= self.graphical_x + self.width:
                if self.graphical_y <= mouse_y <= self.graphical_y + self.height:  # Если клик внутри кнопки
                    self.function()

    # --- Графика ---
    def draw(self):
        """
        Рисует кнопку
        """

        rect(self.inventory.hero.game.screen, self.color, (self.graphical_x, self.graphical_y, self.width, self.height))

    # --- Обработка ---
    def process(self):
        """
        Обрабатывает события кнопки
        """

        self.draw()
        self.manage_click()
