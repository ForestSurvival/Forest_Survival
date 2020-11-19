"""
Модуль яблока
"""

from pygame.draw import *


class Apple(object):
    """
    Описывает яблоко
    """

    def __init__(self, screen, x: float, y: float):
        """
        Параметры

        Координаты центра яблока

        x - координата x яблока в [м]
        y - координата y яблока в [м]
        screen - экран pygame
        """

        self.color: tuple = (5, 95, 23)  # Цвет яблока
        self.radius: int = 5  # Радиус яблока в [px]
        self.satiety: float = 196.7796  # Пищевая энергетическая ценность в [Дж]
        self.screen = screen
        self.x: float = x
        self.y: float = y

    # --- Логика ---
    def process_action(self, forest, hero):
        """
        Описывает взаимодействие героя и яблака

        forest - объект леса
        hero - Объект героя
        """

        hero.inventory.apples_amount += 1  # Добавить яблоко в инвентарь героя
        forest.items_list.remove(self)

    # --- Графика ---
    def draw(self, x: int, y: int):
        """
        Рисует яблоко

        x - координата яблока в [px]
        y - координата яблока в [px]
        """

        circle(self.screen, self.color, (x, y), self.radius)
