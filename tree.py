"""
Модуль дерева
"""
import pygame

from random import *


class Tree(object):
    """
    Описывает дерево
    """

    def __init__(self, forest, physical_x: float, physical_y: float):
        """
        Параметры

        forest - объект леса
        physical_x - физическая координата x дерева в [м]
        physical_y - физическая координата y дерева в [м]
        """

        # Графика
        self.graphical_width: int = 126 * 2 // 3  # Графическая высота дерева в [px]
        self.graphical_height: int = 167 * 2 // 3  # Графическая ширина дерева в [px]

        # Изображения деревьев
        self.images_trees_list = [pygame.image.load('Sprites/Trees/tree_1.bmp'),
                                  pygame.image.load('Sprites/Trees/tree_2.bmp'),
                                  pygame.image.load('Sprites/Trees/tree_3.bmp'),
                                  pygame.image.load('Sprites/Trees/tree_4.bmp')]
        self.image = None

        # Объекты
        self.forest = forest

        # Физика
        self.physical_x: float = physical_x
        self.physical_y: float = physical_y

    # --- Инициализация ---
    def setup(self):
        """
        Присваивает каждому дереву случайное изображение из списка
        """

        self.image = self.images_trees_list[randint(0, 3)]

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует дерево

        graphical_x - графическая координата x дерева в px]
        graphical_y - графическая координата y дерева в [px]
        """

        self.forest.game.graphic_engine.draw_image(self.image, graphical_x, graphical_y, self.graphical_width,
                                                   self.graphical_height)

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события дерева

        graphical_x - графическая координата x дерева в px]
        graphical_y - графическая координата y дерева в [px]
        """

        self.draw(graphical_x, graphical_y)
