"""
Модуль кнопки
"""
# import pygame
#
# from pygame.draw import *


class Button(object):
    """
    Описывает кнопку
    """

    def __init__(self, function, logic_engine, graphic_engine, image, graphical_x: int, graphical_y: int,
                 width: int, height: int):
        """
        Параметры

        function - функция кнопки
        logic_engine - объект логического движка
        graphic_engine - объект графического движка
        image - изображение кнопки
        graphical_x - графическая координата x копки в [px]
        graphical_y - графическая координата y кнопки в [px]
        width - ширина изображения кнопки в [px]
        height - высота изображения кнопки в [px]
        """

        # Логика
        self.function = function

        # Физика
        self.graphical_height: int = height  # Графическая высота кнопки в [px]
        self.graphical_width: int = width  # Графическая ширина кнопки в [px]
        self.graphical_x: int = graphical_x
        self.graphical_y: int = graphical_y

        # Объекты
        self.graphic_engine = graphic_engine
        self.logic_engine = logic_engine

        # Графика
        self.image_button = image

    # --- Логика ---
    def manage_click(self):
        """
        Обрабатывает нажатие
        """

        mouse_pos: list = self.logic_engine.mouse_pos_list  # Список координат мыши
        if mouse_pos != [None]:  # Если кнопка мыши нажата
            mouse_x: int = mouse_pos[0]  # Координата x мыши в [px]
            mouse_y: int = mouse_pos[1]  # Координата y мыши в [px]
            if self.graphical_x <= mouse_x <= self.graphical_x + self.graphical_width:
                if self.graphical_y <= mouse_y <= self.graphical_y + self.graphical_height:  # Если клик внутри кнопки
                    self.function()

    # --- Графика ---
    def draw(self):
        """
        Рисует кнопку

        screen - экран Pygame
        """

        self.graphic_engine.draw_image_corner(self.image_button, self.graphical_x, self.graphical_y,
                                              self.graphical_width, self.graphical_height)

    # --- Обработка ---
    def process(self):
        """
        Обрабатывает события кнопки

        screen - экран Pygame
        """

        self.draw()
        self.manage_click()
