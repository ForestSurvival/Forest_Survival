"""
Модуль костра
"""

import pygame


class Campfire(object):
    """
    Описывает костёр
    """

    def __init__(self, inventory, physical_x: float, physical_y: float):
        """
        Параметры

        inventory - объект инвентаря
        physical_x - физическая координата x костра в [м]
        physical_y - физическая координата y костра в [м]
        """

        # Физика
        self.burn_time_left: float = 10800  # Игровое время горения костра в [с]
        self.physical_x: float = physical_x
        self.physical_y: float = physical_y
        self.matches_amount: int = 1  # Необходимое количество спичек
        self.paper_amount: int = 1  # Необходимое колчество бумаги
        self.safe_distance: float = 1  # Минимальное расстояние, на которое герой может подойти к костру в [м]
        self.sticks_amount: int = 5  # Необходимое количество палок
        self.temperature: float = 573  # Температура костра
        self.temperature_constant = 0.1  # Пропорциональность между темпрературами костра и среды в [м^2]
        self.temperature_burnout: float = 373  # Температура костра при потухании в [К]
        self.cooling_speed = None  # Скорость изменения температуры в [К/с] определяется в campfire.setup()

        # Графика
        self.graphical_height: int = 20  # Графическая высота костра в [px]
        self.graphical_width: int = 20  # Графическая ширина костра в [px]

        # Изображение палки в формате bmp
        self.image_campfire = pygame.image.load('Sprites/campfire.bmp')

        # Объекты
        self.inventory = inventory  # Объект инвентаря

    # --- Инициализация ---
    def count_cooling_speed(self):
        """
        Вычисляет скорость охлаждения костра
        """

        # Разность начальной и конечной температур в [К]
        temperature_range: float = self.temperature - self.temperature_burnout

        self.cooling_speed: float = temperature_range / self.burn_time_left  # Скорость охлаждения в [К/с]

    def setup(self):
        """
        Инициализация костра
        """

        self.count_cooling_speed()

    # --- Логика ---
    def get_created(self):
        """
        Герой создаёт костёр
        """

        self.inventory.hero.game.forest.campfires_list.append(self)

    # --- Физика ---
    def burn(self):
        """
        Костёр горит
        """

        # Объекты
        physical_engine = self.inventory.hero.game.physical_engine  # Объект физического движка

        # Физика
        game_time_delta: float = physical_engine.time_step * physical_engine.time_scale  # Шаг игрового времени в [с]

        self.burn_time_left -= game_time_delta  # Оставшееся игровое время горения костра в [с]
        self.temperature -= self.cooling_speed * game_time_delta  # Костёр остывает
        if self.burn_time_left <= 0:  # Если костёр сгорел
            self.burn_out()

    def burn_out(self):
        """
        Костёр сгорел
        """

        self.inventory.hero.game.forest.campfires_list.remove(self)

    # --- Графика ---
    def draw(self, graphical_x: int, graphical_y: int):
        """
        Рисует костёр

        graphical_x - графическая координата x костра в [px]
        graphical_y - графическая координата y костра в [px]
        """

        # Объекты
        self.inventory.hero.game.graphic_engine.draw_image(self.image_campfire, graphical_x, graphical_y,
                                                           self.graphical_width, self.graphical_height)

    # --- Физика ---
    def melt_snow(self):
        """
        Растопить снег
        """

        self.inventory.water_amount += 1  # Добавить воду в инвентарь
        self.burn_out()

    # --- Обработка ---
    def manage_graphics(self, graphical_x: int, graphical_y: int):
        """
        Обрабатывает графические события костра

        graphical_x - графическая координата x костра в [px]
        graphical_y - графическая координата y костра в [px]
        """

        self.draw(graphical_x, graphical_y)

    def manage_logic(self):
        """
        Обрабатывает логические события костра
        """

        self.melt_snow()

    def process(self):
        """
        Обрабатывает события костра
        """

        self.burn()
