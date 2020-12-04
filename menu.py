"""
Модуль меню
"""

from pygame.draw import *
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
        self.font = None  # Шрифт определяется в menu.setup()

        # Логика
        self.status: str = 'main'  # Определяет окно, которое открыто

        # Объекты
        self.button_play = None  # Кнопка запуска игры определяется в menu.setup()
        self.button_rules = None  # Кнопка правил определяется в menu.setup()
        self.button_rules_exit = None  # Кнопка закрытия окна с правилами определяется в menu.setup()
        self.button_exit = None  # Кнопка выхода из игры определяется в menu.setup()
        self.game = game

    # --- Инициализация ---
    def set_font(self):
        """
        Создаёт шрифт
        """

        font_name = None  # Имя шрифта
        font_size: int = 36  # Размер шрифта
        self.font = Font(font_name, font_size)

    def setup(self):
        """
        Инициализация меню
        """

        self.button_exit = Button(self.game.exit, self.game.logic_engine, 0, 120)  # Кнопка выхода из игры
        self.button_play = Button(self.game.play, self.game.logic_engine, 0, 40)  # Кнопка запуска игры
        self.button_rules = Button(self.switch_to_rules, self.game.logic_engine, 0, 80)  # Кнопка правил

        # Кнопка закрытия окна с правилами
        self.button_rules_exit = Button(self.switch_to_main, self.game.logic_engine, 0, 280)

        self.set_font()

    # --- Графика ---
    def draw_background(self):
        """
        Рисует фон
        """

        color: tuple = (111, 253, 255)  # Цвет фона
        height: int = self.game.graphic_engine.screen.get_height()  # Высота экрана в [px]
        width: int = self.game.graphic_engine.screen.get_width()  # Ширина экрана в [px]
        rect(self.game.graphic_engine.screen, color, (0, 0, width, height))

    def print_text(self, text_str: str, graphical_x: int, graphical_y: int):
        """
        Печатает текст

        text_str - текст, который нужно напечатать
        graphical_x - графическая координата x текста в [px]
        graphical_y - графическая координата y текста в [px]
        """

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

    def manage_logic(self, screen):
        """
        Обрабатывает логические события меню

        screen - экран Pygame
        """

        if self.status == 'main':  # Если игрок в главном меню
            self.button_play.process(screen)
            self.button_rules.process(screen)
            self.button_exit.process(screen)
            self.print_text('Play', 0, 40)
            self.print_text('Rules', 0, 80)
            self.print_text('Exit', 0, 120)
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
            self.button_rules_exit.process(screen)
            self.print_text('Menu', 0, 280)
