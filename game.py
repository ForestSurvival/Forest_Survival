"""
Модуль игры
"""

import pygame


class Game(object):
    """
    Описывает игру
    """

    def __init__(self, screen):
        """
        Параметры

        screen - экран pygame
        """

        # Логика
        self.clock = pygame.time.Clock()  # Часы pygame
        self.status: str = 'created'  # Игра созднана

        # Графика
        self.black: tuple = (0, 0, 0)  # Чёрный цвет
        self.fps: int = 60  # Частота обновления экарана в [Гц]
        self.screen = screen

        # Физика
        self.day_length: int = 600  # Длинна дня в [с]
        self.time_step: float = 1 / self.fps  # Квант времени в [с]

    # --- Логика ---
    def finish(self):
        """
        Завершает игру
        """

        self.status: str = 'finished'  # Игра завершена

    def setup(self):
        """
        Действия при создании игры
        """

        self.status: str = 'forest'  # Маркер основного состояния игры

    def update_logic(self):
        """
        Обрабатывает логические события
        """

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # Если нажата клавиша
                if event.key == pygame.K_ESCAPE:  # Если нажат Esc
                    if self.status == 'forest':  # Если игра находится в основном состоянии
                        self.status: str = 'finished'  # Игра завершена
                    else:
                        self.status: str = 'forest'  # Основное состояние игры
                if event.key == pygame.K_i:  # Если нажата I
                    self.status: str = 'inventory'

    # --- Графика ---
    def update_graphics(self):
        """
        Обновляет экран
        """

        pygame.display.update()
        self.clock.tick(self.fps)
        self.screen.fill(self.black)

    # --- Обработка ---
    def log(self):
        """
        Выводит данные в консоль для отладки
        """

        print('Status:', self.status)
        print('--- Game cycle ---')

    def process(self):
        """
        Обрабатывает события игры
        """

        self.update_logic()
        self.update_graphics()

        # Отладка
        # self.log()
