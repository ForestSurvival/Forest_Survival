"""
Модуль графического движка
"""

import pygame


class GraphicEngine(object):
    """
    Опиывает графический движок
    """

    def __init__(self, game):
        """
        Параметры

        game - объект игры
        """

        self.screen_height: int = 700  # Высота экрана в пикселях
        self.screen_width: int = 1200  # Ширина экрана в пикселях
        self.screen = None  # Определяется в game.setup()

        # Объекты
        self.game = game

    # --- Инициализация ---
    def setup(self):
        """
        Инициализация графического движка
        """

        self.set_screen()

    def set_screen(self):
        """
        Создаёт объект экрана
        """

        # Объект экрана pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    # --- Графика ---
    def draw_image(self, image_load, graphical_x: int, graphical_y: int, width: int, height: int):
        """
        Рисует объект

        image_load - Загруженное изображение
        graphical_x - Графическая координата x объекта в [px]
        graphical_y - Графическая координата y объекта в [px]
        width - Необходимая ширина изображения в [px]
        height - Необходимая высота изображения в [px]
        """

        image_transformed = self.transform(image_load, width, height)  # Изменяет размеры изображения

        graphical_x -= width // 2
        graphical_y -= height // 2

        self.screen.blit(image_transformed, (graphical_x, graphical_y))  # Вставляет изображение объекта

    @staticmethod
    def transform(image_load, width: float, height: float):
        """
        Изменяет размер изображения
        """

        image_transformed = pygame.transform.scale(image_load, (height, width))
        return image_transformed
