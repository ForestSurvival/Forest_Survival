"""
Модуль индикаторов
"""

import pygame

from pygame.draw import *
from pygame.font import *

pygame.font.init()


class Indicator(object):
    """
    Описывает индикатор
    """

    def __init__(self, name, screen, value: float, x: int, y: int):
        """
        Параметры

        Координаты левого верхнего угла индикатора

        name - название индикатора
        screen - экран pygame
        value - значение индицируемой величины в [%]
        x - координата x индикатора в [px]
        y - координата y индикатора в [px]
        """

        # Логика
        self.value: float = value

        # Графика
        self.color_active: tuple = (27, 60, 24)  # Цвет активной части
        self.color_passive: tuple = (0, 0, 0)  # Цвет пассивной части - чёрный
        self.height: int = 36  # Высота индикатора в [px]
        self.width_full: int = 100  # Полная длина индикатора в [px]
        self.x: int = x
        self.y: int = y
        self.screen = screen

        # Текст
        self.font_name = None  # Название шрифта
        self.font_smoothing: bool = True  # Сглаживание шрифта
        self.name: str = name
        self.text_space: int = 10  # Ширина пробела между индикатором и его названием

    # --- Графика ---
    def draw(self):
        """
        Рисует индикатор
        """

        width_active: float = self.width_full * self.value // 100  # Длина активной части в [px]
        width_active_int: int = round(width_active)  # Округлённая длина активной части в [px]

        # Пассивная часть индикатора
        rect(self.screen, self.color_passive, (self.x, self.y, self.width_full, self.height))

        # Активная часть индикатора
        rect(self.screen, self.color_active, (self.x, self.y, width_active_int, self.height))

    def print_name(self):
        """
        Выводит на экран название индикатора
        """

        font = Font(self.font_name, self.height)  # Шрифт pygame
        text_x: int = self.x + self.width_full + self.text_space  # Координата x названия в [px]
        text = font.render(self.name, self.font_smoothing, self.color_active)

        self.screen.blit(text, (text_x, self.y))

    # --- Обработка ---
    def log(self):
        """
        Выводит данные в консоль для отладки
        """

        print('Width active int:', self.width_full)
        print('--- Game cycle ---')

    def process(self):
        """
        Обрабатывает события индикатора
        """

        self.draw()
        self.print_name()

        # Отладка
        # self.log()
