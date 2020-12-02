"""
Главный модуль
"""

import pygame

from game import Game

# Объекты
game = Game()  # Объект игры
game.setup()

while game.status != 'exit':  # Пока игра не завершена
    game.process()
pygame.quit()
