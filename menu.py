"""
Модуль меню
"""
import pygame

from pygame.font import *

from button import Button


class Menu(object):
    """
    Описывает меню
    """

    def __init__(self, game):
        """
        Параметры

        game - объект игры
        """

        # Графика
        self.graphical_height: int = 40  # Графическая высота кнопки в [px]
        self.graphical_width: int = 400  # Графическая ширина кнопки в [px]
        self.font = None  # Шрифт определяется в menu.setup()
        self.image_intro = pygame.image.load('Sprites/intro.bmp')  # Изображение заставки в формате bmp

        self.play_graphical_x = None  # Графическая координата x кнопки play в [px]
        self.play_graphical_y = None  # Графическая координата y кнопки play в [px]
        self.rules_graphical_x = None  # Графическая координата x кнопки rules в [px]
        self.rules_graphical_y = None  # Графическая координата y кнопки rules в [px]
        self.rules_exit_graphical_x = None  # Графическая координата x кнопки rules exit в [px]
        self.rules_exit_graphical_y = None  # Графическая координата y кнопки rules exit в [px]
        self.exit_graphical_x = None  # Графическая координата x кнопки exit в [px]
        self.exit_graphical_y = None  # Графическая координата y кнопки exit в [px]
        self.setup_graphical_x = None  # Графическая координата x кнопки новой игры в [px]
        self.setup_graphical_y = None  # Графическая координата y кнопки новой игры в [px]

        # Логика
        self.status: str = 'main'  # Определяет окно, которое открыто

        # Объекты
        self.button_play = None  # Кнопка запуска игры определяется в menu.setup()
        self.button_rules = None  # Кнопка правил определяется в menu.setup()
        self.button_rules_exit = None  # Кнопка закрытия окна с правилами определяется в menu.setup()
        self.button_setup = None  # Кнопка новой игры определяется в menu.setup()
        self.button_exit = None  # Кнопка выхода из игры определяется в menu.setup()
        self.game = game

        # Текст
        self.font_size = None

        # Физика
        self.screen_width = None  # Ширина экрана в [px]
        self.screen_height = None  # Высота экрана в [px]

    # --- Инициализация ---
    def set_font(self):
        """
        Создаёт шрифт
        """

        font_name = None  # Имя шрифта
        self.font_size: int = 36  # Размер шрифта
        self.font = Font(font_name, self.font_size)

    def setup(self):
        """
        Инициализация меню
        """

        self.set_screen()  # Определяет экран
        self.set_coordinates()  # Определяет координаты кнопок
        self.create_button()  # Создание кнопок
        self.set_font()

    def create_button(self):
        """
        Создание кнопок
        """

        # Кнопка выхода из игры
        self.button_exit = Button(self.game.exit, self.game.logic_engine, self.game.graphic_engine,
                                  self.game, self.exit_graphical_x, self.exit_graphical_y,
                                  self.graphical_width, self.graphical_height)

        # Кнопка запуска игры
        self.button_play = Button(self.game.play, self.game.logic_engine, self.game.graphic_engine,
                                  self.game, self.play_graphical_x, self.play_graphical_y,
                                  self.graphical_width, self.graphical_height)

        # Кнопка правил
        self.button_rules = Button(self.switch_to_rules, self.game.logic_engine, self.game.graphic_engine,
                                   self.game, self.rules_graphical_x, self.rules_graphical_y,
                                   self.graphical_width, self.graphical_height)

        # Кнопка закрытия окна с правилами
        self.button_rules_exit = Button(self.switch_to_main, self.game.logic_engine, self.game.graphic_engine,
                                        self.game, self.rules_exit_graphical_x, self.rules_exit_graphical_y,
                                        self.graphical_width, self.graphical_height)

        # Кнопка новой игры
        self.button_setup = Button(self.game.setup, self.game.logic_engine, self.game.graphic_engine,
                                   self.game, self.setup_graphical_x, self.setup_graphical_y,
                                   self.graphical_width, self.graphical_height)

    def set_coordinates(self):
        """
        Определение координат кнопок
        """

        self.play_graphical_x: int = (self.screen_width - self.graphical_width) // 2
        self.play_graphical_y = 200
        self.rules_graphical_x: int = (self.screen_width - self.graphical_width) // 4
        self.rules_graphical_y = 350
        self.rules_exit_graphical_x: int = (self.screen_width - self.graphical_width) // 2
        self.rules_exit_graphical_y = 350
        self.exit_graphical_x: int = (self.screen_width - self.graphical_width) * 3 // 4
        self.exit_graphical_y = 500
        self.setup_graphical_x: int = 0
        self.setup_graphical_y: int = 80

    def set_screen(self):
        """
        Определение параметров экрана
        """

        self.screen_width: int = self.game.graphic_engine.screen_width
        self.screen_height: int = self.game.graphic_engine.screen_height

    # --- Графика ---
    def draw_background(self):
        """
        Рисует фон
        """

        height: int = self.game.graphic_engine.screen.get_height()  # Высота экрана в [px]
        width: int = self.game.graphic_engine.screen.get_width()  # Ширина экрана в [px]
        graphical_x: int = 0
        graphical_y: int = 0

        self.game.graphic_engine.draw_image_corner(self.image_intro, graphical_x, graphical_y, width, height)

    def print_text(self, text_str: str, graphical_x: int, graphical_y: int):
        """
        Печатает текст

        text_str - текст, который нужно напечатать
        graphical_x - графическая координата x текста в [px]
        graphical_y - графическая координата y текста в [px]
        """

        graphical_x += (self.graphical_width // 2 - self.font_size)
        graphical_y += (self.graphical_height - self.font_size // 2) // 2

        color: tuple = (79, 70, 202)  # Цвет текста
        smoothing: bool = True  # Нужно ли сглаживать текст
        text = self.font.render(text_str, smoothing, color)  # Объект текста
        self.game.graphic_engine.screen.blit(text, (graphical_x, graphical_y))

    # --- Логика ---
    def switch_to_main(self):
        """
        Выходит в главное меню
        """

        self.status: str = 'main'  # Выйти в главное меню

    def switch_to_rules(self):
        """
        Показывает правила игры
        """

        self.status: str = 'rules'  # Показать правила

    # --- Обработка ---
    def manage_graphics(self):
        """
        Обрабатывает графические события меню
        """

        self.draw_background()
        self.print_text('Forest Survival', 0, 0)

    def manage_logic(self):
        """
        Обрабатывает логические события меню

        screen - экран Pygame
        """

        if self.status == 'main':  # Если игрок в главном меню
            self.button_play.process()
            self.button_rules.process()
            self.button_exit.process()
            self.print_text('Play', self.play_graphical_x, self.play_graphical_y)
            self.print_text('Rules', self.rules_graphical_x, self.rules_graphical_y)
            self.print_text('Exit', self.exit_graphical_x, self.exit_graphical_y)
        elif self.status == 'rules':  # Если игрок читает правила
            self.print_text('Rules', 0, 40)
            self.print_text('1) You can be dead from starvation. Find food in the forest and eat it to increase your '
                            'satiety', 0, 80)
            self.print_text('2) You can be dead from thirst. You need to burn the campfire and melt the snow down to '
                            'get water', 0, 120)
            self.print_text('3) To burn the campfire you need to find 5 sticks in the forest, 1 match and 1 piece of '
                            'paper', 0, 160)
            self.print_text('   in the house', 0, 200)
            self.print_text('4) To win the game you need to find the village and get out of the forest', 0, 240)
            self.button_rules_exit.process()
            self.print_text('Menu', self.rules_exit_graphical_x, self.rules_exit_graphical_y)
        elif self.status == 'dead':  # Если герой мёртв
            self.button_setup.process()
            self.print_text('Вы мертвы', 0, 40)
            self.print_text('Вернуться в меню', 0, 80)
