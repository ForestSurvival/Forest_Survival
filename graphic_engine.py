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

        # Спрайты
        self.game_background = pygame.image.load('Sprites/game_background.png')  # Изображение фона в формате png

        # Объекты
        self.game = game

    # --- Инициализация ---
    def setup(self):
        """
        Инициализация графического движка
        """

        self.set_screen()
        self.set_draw_background()

    def set_draw_background(self):
        """
        Рисует фон игры
        """

        # self.transform(self.game_background, self.screen_width, self.screen_height)
        # self.draw_picture(self.game_background, 0, 0)
        self.screen.fill((255, 100, 210))

    def set_screen(self):
        """
        Создаёт объект экрана
        """

        # Объект экрана pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)

    # --- Графика ---
    def draw_picture(self, picture, grafical_x: int, grafical_y: int):
        """
        Рисует объект

        graphical_x - Графическая координата x объекта в [px]
        graphical_y - Графическая координата y объекта в [px]
        """

        print(grafical_x, grafical_y)
        self.screen.blit(picture, (grafical_x, grafical_y))  # Вставляет изображение объекта

    def transform(self, picture, width: float, height: float):
        """
        Изменяет размер изображения
        """

        picture = pygame.transform.scale(picture, (width, height))
        return picture

    # --- Логика ---
    def manage_graphic(self):
        """
        Обрабатывает графические события
        """

        # Обработка фона
        # self.transform(self.game_background, self.screen_width, self.screen_height)
        # self.draw_picture(self.game_background, 300, 200)
        pass

    # --- Обработка ---
    def process(self):
        """
        Обрабатывает события графического движка
        """

        self.manage_graphic()