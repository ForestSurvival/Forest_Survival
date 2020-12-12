"""
Модуль инвентаря
"""

import pygame

from pygame.font import *

from button import Button
from campfire import Campfire
from water import Water


class Inventory(object):
    """
    Описывает инвентарь
    """

    def __init__(self, hero):
        """
        Параметры

        hero - объект героя
        """

        # Физика
        self.apples_amount: int = 0  # Количество яблок
        self.matches_amount: int = 0  # Количество спичек
        self.paper_amount: int = 0  # Количество бумаги
        self.sticks_amount: int = 0  # Количество палок
        self.water_amount: int = 0  # Количество воды
        self.screen_width = None  # Ширина экрана в [px]
        self.screen_height = None  # Высота экрана в [px]

        # Графика
        self.apple_graphical_x: int = 30  # Графическая координата x записи о яблоке в [px]
        self.apple_graphical_y: int = 80  # Графическая координата y записи о яблоке в [px]
        self.campfire_graphical_x: int = 490  # Графическая координата x записи о костре в [px]
        self.campfire_graphical_y: int = 80  # Графическая координата y записи о косте в [px]
        self.match_graphical_x: int = 30  # Графическая координата x записи о спичке в [px]
        self.match_graphical_y: int = 150  # Графическая координата y записи о спичке в [px]
        self.paper_graphical_x: int = 260  # Графическая координата x записи о бумаге в [px]
        self.paper_graphical_y: int = 150  # Графическая координата y записи о бумаге в [px]
        self.stick_graphical_x: int = 490  # Графическая коордиата x записи о палке в [px]
        self.stick_graphical_y: int = 150  # Графическая координата y записи о палке в [px]
        self.water_graphical_x: int = 260  # Графическая коордиата x записи о воде в [px]
        self.water_graphical_y: int = 80  # Графическая координата y записи о воде в [px]
        self.temp_graphical_x: int = 700  # Графическая коордиата x записи о температуре воздуха в [px]
        self.temp_graphical_y: int = 130  # Графическая координата y записи о температуре воздуха в [px]

        self.graphical_height: int = 40  # Графическая высота кнопки в [px]
        self.graphical_width: int = 100  # Графическая ширина кнопки в [px]

        self.image_inventory = pygame.image.load('Sprites/inventory.bmp')  # Изображение заставки в формате bmp

        # Текст
        self.font_size = 32  # Размер шрифта
        self.text_space_x = 30  # Ширина пробела между изображением объекта и записью о количестве его копий в [px]
        self.text_space_y = 8

        # Объекты
        self.apple = None  # Объект яблока определяется в inventory.setup()

        # Объект кнопки яблока
        self.button_apple = None  # Объект кнопки яблока определяется в inventory.setup()

        self.button_campfire = None  # Кнопка разведения костра определяется в inventory.setup()
        self.button_water = None  # Кнопка воды определяется в inventory.setup()
        self.campfire = Campfire(self, 0, 0)  # Объект костра
        self.hero = hero  # Объект героя
        self.match = None  # Объект спички определяется в inventory.setup()
        self.paper = None  # Объект бумаги определяется в inventory.setup()
        self.stick = None  # Объект палки определяется в inventory.setup()
        self.water = Water(self)

    # --- Инициализация ---
    def get_object(self, item_name: str):
        """
        Определяет объекта

        item_name - название объекта
        """

        # Объекты
        items_dict: dict = {'apple': self.hero.game.forest.apples_list[0],  # Словарь объектов
                            'match': self.hero.game.forest.houses_list[0].match,
                            'paper': self.hero.game.forest.houses_list[0].paper,
                            'stick': self.hero.game.forest.sticks_list[0]}

        defined_object = items_dict[item_name]  # Определённый объект
        return defined_object

    def setup(self):
        """
        Инициализация инвентаря
        """

        self.set_screen()

        self.apple = self.get_object('apple')
        self.match = self.get_object('match')
        self.paper = self.get_object('paper')
        self.stick = self.get_object('stick')

        # Объект кнопки яблока
        self.button_apple = Button(self.hero.eat_apple, self.hero.game.logic_engine, self.hero.game.graphic_engine,
                                   self.hero.game, self.apple_graphical_x, self.apple_graphical_y,
                                   self.graphical_width, self.graphical_height)

        # Объект кнопки костра
        self.button_campfire = Button(self.hero.burn_campfire, self.hero.game.logic_engine,
                                      self.hero.game.graphic_engine, self.hero.game,
                                      self.campfire_graphical_x, self.campfire_graphical_y,
                                      self.graphical_width, self.graphical_height)

        # Объект кнопки воды
        self.button_water = Button(self.hero.drink_water, self.hero.game.logic_engine, self.hero.game.graphic_engine,
                                   self.hero.game, self.water_graphical_x, self.water_graphical_y,
                                   self.graphical_width, self.graphical_height)

    def set_screen(self):
        """
        Определение параметров экрана
        """

        self.screen_width = self.hero.game.graphic_engine.screen_width
        self.screen_height = self.hero.game.graphic_engine.screen_height

    # --- Графика ---
    def draw_background(self):
        """
        Рисует фон
        """

        height: int = self.hero.game.graphic_engine.screen.get_height()  # Высота экрана в [px]
        width: int = self.hero.game.graphic_engine.screen.get_width()  # Ширина экрана в [px]
        graphical_x: int = 0
        graphical_y: int = 0

        self.hero.game.graphic_engine.draw_image_corner(self.image_inventory, graphical_x, graphical_y, width, height)

    def print_text(self, graphical_x: int, graphical_y: int, text_str: str):
        """
        Печатает текст на экране

        graphical_x - графическая координата x текста в [px]
        graphical_y - графическая координата y текста в [px]
        text_str - текст
        """

        # Графика
        font = self.set_font()
        font_smoothing: bool = True  # Сглаживание шрифта
        text_color: tuple = (20, 0, 30)  # Цвет текста

        text = font.render(text_str, font_smoothing, text_color)  # Текст в формате Pygame
        self.hero.game.graphic_engine.screen.blit(text, (graphical_x, graphical_y))

    def set_font(self):
        """
        Создаёт шрифт
        """

        # Графика
        font_name = "Fonts/GARABD.ttf"  # Имя шрифта

        font = Font(font_name, self.font_size)  # Шрифт
        return font

    def show_object(self, object_name):
        """
        Показывает информацию об объекте

        object_name - название объекта
        """

        # Объекты
        apple_dict: dict = {'amount': self.apples_amount,  # Словарь яблока
                            'graphical_x': self.apple_graphical_x - self.graphical_width // 8,
                            'graphical_y': self.apple_graphical_y + self.graphical_height // 2,
                            'name': self.apple}
        campfire_dict: dict = {'amount': None,  # Словарь яблока
                               'graphical_x': self.campfire_graphical_x - self.graphical_width // 8,
                               'graphical_y': self.campfire_graphical_y + self.graphical_height // 2,
                               'name': self.campfire}
        match_dict: dict = {'amount': self.matches_amount,  # Словарь спички
                            'graphical_x': self.match_graphical_x - self.graphical_width // 8,
                            'graphical_y': self.match_graphical_y + self.graphical_height // 2,
                            'name': self.match}
        paper_dict: dict = {'amount': self.paper_amount,  # Словарь бумаги
                            'graphical_x': self.paper_graphical_x - self.graphical_width // 8,
                            'graphical_y': self.paper_graphical_y + self.graphical_height // 2,
                            'name': self.paper}
        stick_dict: dict = {'amount': self.sticks_amount,  # Словарь палки
                            'graphical_x': self.stick_graphical_x - self.graphical_width // 8,
                            'graphical_y': self.stick_graphical_y + self.graphical_height // 2,
                            'name': self.stick}
        water_dict: dict = {'amount': self.water_amount,  # Словарь воды
                            'graphical_x': self.water_graphical_x - self.graphical_width // 8,
                            'graphical_y': self.water_graphical_y + self.graphical_height // 2,
                            'name': self.water}
        objects_dict: dict = {'apple': apple_dict,  # Словарь объектов
                              'campfire': campfire_dict,
                              'match': match_dict,
                              'paper': paper_dict,
                              'stick': stick_dict,
                              'water': water_dict}

        item_dict: dict = objects_dict[object_name]  # Словарь объекта, информацию о котором нужно показать
        item_dict['name'].draw(item_dict['graphical_x'], item_dict['graphical_y'])

        # Графические координаты текста в [px]
        text_graphical_x = item_dict['graphical_x'] + item_dict['name'].graphical_width + self.text_space_x
        text_graphical_y = item_dict['graphical_y'] - item_dict['name'].graphical_width + self.text_space_y

        item_dict['name'].draw(item_dict['graphical_x'], item_dict['graphical_y'])
        if item_dict['amount'] is not None:  # Если у объекта определено количество
            amount_str: str = str(item_dict['amount'])  # Количество объектов
            self.print_text(text_graphical_x, text_graphical_y, amount_str)

    # --- Обработка ---
    def manage_graphics(self):
        """
        Обабатывает графические события инвентаря
        """

        self.draw_background()
        self.button_apple.process()
        self.button_campfire.process()
        self.button_water.process()
        self.show_object('apple')
        self.show_object('campfire')
        self.show_object('match')
        self.show_object('paper')
        self.show_object('stick')
        self.show_object('water')
        temperature: float = self.hero.game.physical_engine.get_local_temperature()  # Температура среды в [К]

        # Температура среды в [С*]
        temperature_celsius: float = temperature + self.hero.game.physical_engine.absolute_zero_celsius

        temperature_round: int = round(temperature_celsius)  # Округлённая температура среды в [С*]
        temperature_str: str = str(temperature_round)  # Строка с температурой среды в [С*]
        self.print_text(self.temp_graphical_x, self.temp_graphical_y, 'Температура: ' + temperature_str + ' C*')

    def process(self):
        """
        Обрабатывает события инвентаря
        """

        self.manage_graphics()
