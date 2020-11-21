"""
Главный модуль
"""

from game import Game

# Объекты
game = Game()  # Объект игры
game.setup()

while game.status != 'exit':  # Пока игра не завершена
    game.process()
