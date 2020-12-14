"""
Модуль кнопки
"""

import pygame


class Button(object):
    """
    Описывает кнопку
    """

    def __init__(self, function, logic_engine, graphic_engine, game, graphical_x: int, graphical_y: int,
                 width: int, height: int):
        """
        Параметры

        function - функция кнопки
        logic_engine - объект логического движка
        graphic_engine - объект графического движка
        graphical_x - графическая координата x кнопки в [px]
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
        self.tick_count = None
        self.tick_count_start = 0

        # Объекты
        self.graphic_engine = graphic_engine
        self.logic_engine = logic_engine
        self.game = game

        # Графика
        self.image_button = pygame.image.load('Sprites/blue_button.bmp')  # Изображение ненажатой кнопки в формате bmp

        # Изображение нажатой кнопки в формате bmp
        self.image_button_pressed = pygame.image.load('Sprites/blue_button_pressed.bmp')
        self.image = self.image_button

        # Звуки
        self.sound_button = pygame.mixer.Sound('Soundtrack/button.wav')

    # --- Инициализация ---
    def setup(self):
        """
        Определяет количество циклов, прошедших с начала игры
        """

        self.tick_count = self.game.tick_count

    # --- Логика ---
    def manage_click(self):
        """
        Обрабатывает нажатие
        """

        mouse_pos: list = self.logic_engine.mouse_pos_list  # Список координат мыши
        if mouse_pos != [None]:  # Если кнопка мыши нажата
            self.sound_button.play()
            self.sound_button.set_volume(0.5)
            mouse_x: int = mouse_pos[0]  # Координата x мыши в [px]
            mouse_y: int = mouse_pos[1]  # Координата y мыши в [px]
            if self.graphical_x <= mouse_x <= self.graphical_x + self.graphical_width:
                if self.graphical_y <= mouse_y <= self.graphical_y + self.graphical_height:  # Если клик внутри кнопки
                    self.function()
                    if self.graphical_width <= 200:
                        self.image = self.image_button_pressed
                        self.tick_count_start = self.tick_count

    # --- Графика ---
    def draw(self):
        """
        Рисует кнопку

        screen - экран Pygame
        """
        
        if self.tick_count - self.tick_count_start >= 6:
            self.image = self.image_button

        self.graphic_engine.draw_image_corner(self.image, self.graphical_x, self.graphical_y,
                                              self.graphical_width, self.graphical_height)

    # --- Обработка ---
    def process(self):
        """
        Обрабатывает события кнопки

        screen - экран Pygame
        """

        self.setup()
        self.draw()
        self.manage_click()
