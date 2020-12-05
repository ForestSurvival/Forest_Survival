"""
Модуль физического движка
"""

from math import sqrt


class PhysicalEngine(object):
    """
    Описывает физический движок
    """

    def __init__(self, game):
        """
        Параметры

        game - объект игры
        """

        # Физика
        self.time_scale: float = 86400 / game.day_length  # Масштаб времени
        self.time_step: float = 1 / game.fps  # Шаг игры по времени

        # Объекты
        self.game = game

    # --- Физика ---
    def find_close_object(self, object_list: list):
        """
        Проверяет, есть ли объект в радиусе действия героя

        object_list - список объектов, которые надо проверить
        """

        # Объекты
        hero = self.game.hero  # Объект героя

        # Фмзика
        hero_physical_x: float = hero.x  # Фихическая координата x героя в [м]
        hero_physical_y: float = hero.y  # Физическая координата y героя в [м]

        for item in object_list:
            object_physical_x: float = item.physical_x  # Физическая координата x объекта в [м]
            object_physical_y: float = item.physical_y  # Фихическая координата y объекта в [м]

            # Проекция физического расстояния между героем и объектом в [м] на ось x
            physical_delta_x: float = hero_physical_x - object_physical_x

            # Проекция физического расстояния между героем и объектом в [м] на ось y
            physical_delta_y: float = hero_physical_y - object_physical_y

            # Физическое расстояние между героем и объектом в [м]
            distance: float = sqrt(physical_delta_x ** 2 + physical_delta_y ** 2)

            if distance <= hero.action_radius:  # Если объект близко к герою
                return item
        return None
