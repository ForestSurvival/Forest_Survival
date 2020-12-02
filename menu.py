"""
Модуль меню
"""

from pygame.draw import *
from pygame.font import *

from button import Button


class Menu(object):
    """
    Описывает меню
    """

    def __init__(self, game):
        """
        Параметры

        game - объект игры
        """

        # Графика
        self.font = None  # Шрифт определяется в menu.setup()

        # Объекты
        self.button_play = None  # Кнопка запуска игры определяется в menu.setup()
        self.game = game

    # --- Инициализация ---
    def set_font(self):
        """
        Создаёт шрифт
        """

        font_name = None  # Имя шрифта
        font_size: int = 36  # Размер шрифта
        self.font = Font(font_name, font_size)

    def setup(self):
        """
        Инициализация меню
        """

        self.button_play = Button(self.game.play, self.game.logic_engine, 0, 40)  # Кнопка запуска игры
        self.set_font()

    # --- Графика ---
    def draw_background(self):
        """
        Рисует фон
        """

        color: tuple = (111, 253, 255)  # Цвет фона
        height: int = self.game.graphic_engine.screen.get_height()  # Высота экрана в [px]
        width: int = self.game.graphic_engine.screen.get_width()  # Ширина экрана в [px]
        rect(self.game.graphic_engine.screen, color, (0, 0, width, height))

    def print_text(self, text_str: str, graphical_x: int, graphical_y: int):
        """
        Печатает текст

        text_str - текст, который нужно напечатать
        graphical_x - графическая координата x текста в [px]
        graphical_y - графическая координата y текста в [px]
        """

        color: tuple = (79, 70, 202)  # Цвет текста
        smoothing: bool = True  # Нужно ли сглаживать текст
        text = self.font.render(text_str, smoothing, color)  # Объект текста
        self.game.graphic_engine.screen.blit(text, (graphical_x, graphical_y))

    # --- Обработка ---
    def manage_graphics(self):
        """
        Обрабатывает графические события меню
        """

        self.draw_background()
        self.print_text('Forest Survival', 0, 0)

    def manage_logic(self, screen):
        """
        Обрабатывает логические события меню

        screen - экран Pygame
        """

        self.button_play.process(screen)
        self.print_text('Play', 0, 40)
