"""
Модуль кнопки
"""

from pygame.draw import *


class Button(object):
    """
    Описывает кнопку
    """

    def __init__(self, function, logic_engine, graphical_x: int, graphical_y: int):
        """
        Параметры

        function - функция кнопки
        logic_engine - объект логического движка
        graphical_x - графическая координата x копки в [px]
        graphical_y - графическая координата y кнопки в [px]
        screen - экран для рисования
        """

        # Логика
        self.function = function

        # Физика
        self.height: int = 30  # Высота кнопки в [px]
        self.width: int = 100  # Ширина кнопки в [px]
        self.graphical_x: int = graphical_x
        self.graphical_y: int = graphical_y

        # Объекты
        self.logic_engine = logic_engine

        # Графика
        self.color: tuple = (203, 247, 72)  # Цвет кнопки

    # --- Логика ---
    def manage_click(self):
        """
        Обрабатывает нажатие
        """

        mouse_pos: list = self.logic_engine.mouse_pos_list  # Список координат мыши
        if mouse_pos != [None]:  # Если кнопка мыши нажата
            mouse_x: int = mouse_pos[0]  # Координата x мыши в [px]
            mouse_y: int = mouse_pos[1]  # Координата y мыши в [px]
            if self.graphical_x <= mouse_x <= self.graphical_x + self.width:
                if self.graphical_y <= mouse_y <= self.graphical_y + self.height:  # Если клик внутри кнопки
                    self.function()

    # --- Графика ---
    def draw(self, screen):
        """
        Рисует кнопку

        screen - экран Pygame
        """

        rect(screen, self.color, (self.graphical_x, self.graphical_y, self.width, self.height))

    # --- Обработка ---
    def process(self, screen):
        """
        Обрабатывает события кнопки

        screen - экран Pygame
        """

        self.draw(screen)
        self.manage_click()
