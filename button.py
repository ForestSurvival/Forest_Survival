"""
Модуль кнопки
"""

from pygame.draw import *


class Button(object):
    """
    Описывает кнопку
    """

    def __init__(self, function, inventory, x: int, y: int):
        """
        Параметры

        function - функция кнопки
        inventory - объект инвентаря
        x - координата x копки в [px]
        y - координата y кнопки в [px]
        """

        self.color: tuple = (203, 247, 72)  # Цвет кнопки
        self.function = function
        self.height: int = 30  # Высота кнопки в [px]
        self.inventory = inventory
        self.width: int = 100  # Ширина кнопки в [px]
        self.x: int = x
        self.y: int = y

    # --- Физика ---
    def manage_click(self):
        """
        Обрабатывает нажатие
        """

        mouse_pos: list = self.inventory.hero.game.logic_engine.mouse_pos_list  # Список координат мыши
        if mouse_pos != [None]:  # Если кнопка мыши нажата
            mouse_x: int = mouse_pos[0]  # Координата x мыши в [px]
            mouse_y: int = mouse_pos[1]  # Координата y мыши в [px]
            if self.x <= mouse_x <= self.x + self.width:
                if self.y <= mouse_y <= self.y + self.height:  # Если клик внутри кнопки
                    self.function()

    # --- Графика ---
    def draw(self):
        """
        Рисует кнопку
        """

        rect(self.inventory.hero.game.screen, self.color, (self.x, self.y, self.width, self.height))

    # --- Обработка ---
    def process(self):
        """
        Обрабатывает события кнопки
        """

        self.draw()
        self.manage_click()
