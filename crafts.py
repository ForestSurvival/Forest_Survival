"""
Модуль крафтов
"""

from pygame.font import *

from button import Button
from campfire import Campfire


class Crafts(object):
    """
    Описывает крафты героя
    """

    def __init__(self, hero):
        """
        Параметры

        hero - объект героя
        """

        # Графика
        self.fire_graphical_x: int = 5  # Графическая координата x записи о костре в [px]
        self.fire_graphical_y: int = 40  # Графическая координата y записи о костере в [px]

        # Текст
        self.font = None  # Шрифт определяется в inventory.setup()
        self.font_smoothing: bool = True  # Сглаживание шрифта
        self.text_color: tuple = (79, 70, 202)  # Цвет текста
        self.text_space = 10  # Ширина пробела между изображением объекта и записью о его требованиях в [px]

        # Объекты
        self.campfire = Campfire(self, hero.x, hero.y)  # Объект костра
        self.button_campfire = Button(self.campfire.get_created, self, self.fire_graphical_x, self.fire_graphical_y)
        self.hero = hero

    # --- Инициализация ---
    def set_font(self):
        """
        Устанавливает шрифт
        """

        font_name = None  # Имя шрифта
        font_size: int = 30  # Размер шрифта
        self.font = Font(font_name, font_size)  # Шрифт Pygame

    def setup(self):
        """
        Инициализация инвентаря
        """

        self.set_font()

    # --- Обработка ---
    def manage_graphics(self):
        """
        Обрабатывает графические события крафтов
        """

        pass

    def manage_logic(self):
        """
        Обрабатывает логические события крафтов
        """

        pass

    def process(self):
        """
        Обрабатывает события крафтов
        """

        pass
