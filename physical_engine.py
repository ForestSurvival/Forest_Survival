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
        self.absolute_zero_celsius: int = -273  # Абсолютный ноль в [С*]
        self.time_scale: float = 86400 / game.day_length  # Масштаб времени
        self.time_step: float = 1 / game.fps  # Шаг игры по времени

        # Объекты
        self.game = game

    # --- Физика ---
    def get_local_temperature(self):
        """
        Вычисляет температуру среды в точке, где находится герой
        """

        campfires_heat_square: float = 0  # Квадрат температуры, создаваемой кострами в [К^2]
        for campfire in self.game.forest.campfires_list:

            x: float = campfire.physical_x  # Координата x костра в [м]
            y: float = campfire.physical_y  # Координата y костра в [м]
            distance: float = self.get_physical_distance(self.game.hero.x, self.game.hero.y, x, y)
            if distance < campfire.safe_distance:  # Если герой подашёл слишком близко к костру
                distance: float = campfire.safe_distance  # Он не сгорит заживо

            # Вклад костра в увеличение температуры
            delta_temperature: float = campfire.temperature_constant * campfire.temperature / distance ** 2

            campfires_heat_square += delta_temperature ** 2  # Складываются квадраты температур
        campfires_heat: float = sqrt(campfires_heat_square)  # Температура, создаваемая всеми кострами в [К]
        house_heat: float = 0  # Вклад дома в повышение температуры
        for house in self.game.forest.houses_list:
            x: float = house.physical_x  # Координата x дома в [м]
            y: float = house.physical_y  # Координата y дома в [м]

            # Расстояние до дома в [м]
            distance: float = self.get_physical_distance(self.game.hero.x, self.game.hero.y, x, y)

            if distance <= house.action_radius:
                house_heat: float = house.temperature  # Вклад дома в повышение в температуры
        temperature: float = self.game.forest.temperature_passive + campfires_heat + house_heat  # Температура среды
        return temperature

    @staticmethod
    def get_physical_distance(physical_x_1: float, physical_y_1: float, physical_x_2: float, physical_y_2: float):
        """
        Вычисляет физическое расстояние в [м] между 2 точками
        :param physical_x_1 - физическая координата x 1 точки в [м]
        :param physical_y_1 - физическая координата y 1 точки в [м]
        :param physical_x_2 - физическая координата x 2 точки в [м]
        :param physical_y_2 - физическая координата y 2 точки в [м]
        """

        distance_x: float = physical_x_1 - physical_x_2  # Физическое расстояние между объектами по оси x в [м]
        distance_y: float = physical_y_1 - physical_y_2  # Физическое расстояние между объектами по оси y в [м]
        distance: float = sqrt(distance_x ** 2 + distance_y ** 2)  # Физическое расстояние между точками в [м]
        return distance

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

    def make_heat_translation(self, temperature: float):
        """
        Выполняет теплообмен между героем и средой

        temperature - температура среды в [К]
        """

        # Объекты
        hero = self.game.hero  # Объект героя

        clothes_temperature: float = temperature + hero.heat_bonus_clothes  # Температура с учётом одежды [К]
        temperature_delta: float = clothes_temperature - hero.temperature  # Разность температур среды и героя в [К]
        heat_power: float = temperature_delta * hero.thermal_conductivity  # Мощность теплообмена в [Вт]
        game_time_delta: float = self.time_step * self.time_scale  # Шаг игрового времени в [с]
        thermal_energy_delta: float = heat_power * game_time_delta  # Расход теплоты в [Дж]

        # Изменение температуры героя в [К]
        hero_temperature_delta: float = thermal_energy_delta / hero.heat_capacity

        # Новая температура героя в [К]
        self.game.hero.temperature: float = min(hero.temperature_max, max(hero.temperature_min,
                                                                          hero.temperature + hero_temperature_delta))

    # --- Обработка ---
    def manage_physics(self):
        """
        Обрабатывает физические события
        """

        temperature: float = self.get_local_temperature()
        self.make_heat_translation(temperature)
