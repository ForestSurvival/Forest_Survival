"""
Модуль индикаторов
"""

import pygame

from pygame.font import *

pygame.font.init()


class Indicator(object):
    """
    Описывает индикатор
    """

    def __init__(self, name, hero, value: float, x: int, y: int):
        """
        Параметры

        Координаты левого верхнего угла индикатора

        name - название индикатора
        hero - объект героя
        value - значение индицируемой величины в [%]
        x - координата x индикатора в [px]
        y - координата y индикатора в [px]
        """

        # Логика
        self.value: float = value
        self.hero = hero

        # Графика
        self.color_text_indicator: tuple = (0, 15, 0)  # Цвет текста индикатора
        self.height: int = 30  # Высота индикатора в [px]
        self.width_full: int = 100  # Полная длина индикатора в [px]
        self.x: int = x
        self.y: int = y
        self.graphical_width: int = 0  # Графическая ширина индикатора в текущий момент в [px]

        # Изображение индикатора в формате bmp
        self.image_indicator = pygame.image.load('Sprites/indicator.bmp')
        self.image_indicator_dark = pygame.image.load('Sprites/indicator_dark.bmp')

        # Текст
        self.font_name = "Fonts/GARABD.TTF"  # Название шрифта
        self.font_size: int = 28  # Размер шрифта
        self.font_smoothing: bool = True  # Сглаживание шрифта
        self.name: str = name
        self.text_space: int = 5  # Ширина пробела между индикатором и его названием

    # --- Графика ---
    def draw(self):
        """
        Рисует индикатор
        """

        width_active: float = self.width_full * self.value // 100  # Длина активной части в [px]
        width_active_int: int = round(width_active)  # Округлённая длина активной части в [px]

        # Пассивная часть индикатора
        self.hero.game.graphic_engine.draw_image_corner(self.image_indicator_dark, self.x, self.y,
                                                        self.width_full, self.height)

        # Активная часть индикатора
        self.hero.game.graphic_engine.draw_image_corner(self.image_indicator, self.x, self.y,
                                                        width_active_int, self.height)

    def print_name(self):
        """
        Выводит на экран название индикатора
        """

        font = Font(self.font_name, self.font_size)  # Шрифт pygame
        text_x: int = self.x + self.width_full + self.text_space  # Координата x названия в [px]
        text = font.render(self.name, self.font_smoothing, self.color_text_indicator)

        self.hero.game.graphic_engine.screen.blit(text, (text_x, self.y))

    def process(self):
        """
        Обрабатывает события индикатора
        """

        self.draw()
        self.print_name()
