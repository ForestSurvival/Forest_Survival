"""
Главный модуль
"""

import pygame

from game import Game

# Графика
screen_height: int = 700  # Высота экрана в пикселях
screen_width: int = 1200  # Ширина экрана в пикселях
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)  # Объект экрана pygame

# Объекты
game = Game(screen)  # Объект игры
game.setup()

while game.status != 'exit':  # Пока игра не завершена
    game.process()
