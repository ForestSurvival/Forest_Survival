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
        self.graphical_height: int = 50  # Графическая высота кнопки в [px]
        self.graphical_width: int = 450  # Графическая ширина кнопки в [px]
        self.font = None  # Шрифт определяется в menu.setup()
        self.font_title = None
        self.image_intro = pygame.image.load('Sprites/intro.bmp')  # Изображение заставки в формате bmp

        self.controls_graphical_x = None  # Координата x кнопки управления в [px]
        self.controls_graphical_y = None  # Координата y кнопки управления в [px]
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
        self.button_controls = None  # Кнопка управления определяется в menu.setup()
        self.button_play = None  # Кнопка запуска игры определяется в menu.setup()
        self.button_rules = None  # Кнопка правил определяется в menu.setup()
        self.button_rules_exit = None  # Кнопка закрытия окна с правилами определяется в menu.setup()
        self.button_setup = None  # Кнопка новой игры определяется в menu.setup()
        self.button_exit = None  # Кнопка выхода из игры определяется в menu.setup()
        self.game = game

        # Текст
        self.text_y = 2
        self.text_x = 70

        # Физика
        self.screen_width = None  # Ширина экрана в [px]
        self.screen_height = None  # Высота экрана в [px]

    # --- Инициализация ---
    def set_font(self):
        """
        Создаёт шрифт
        """

        font_name = "Fonts/GARABD.ttf"  # Имя шрифта
        font_name_title = "Fonts/VINERITC.ttf"  # Имя шрифта заголовка
        font_size: int = 36  # Размер шрифта
        font_size_title: int = 70
        self.font = Font(font_name, font_size)
        self.font_title = Font(font_name_title, font_size_title)

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

        # Кнопка управления
        self.button_controls = Button(self.switch_to_controls, self.game.logic_engine, self.game.graphic_engine,
                                      self.game, self.controls_graphical_x, self.controls_graphical_y,
                                      self.graphical_width, self.graphical_height)

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

        self.controls_graphical_x: int = (self.screen_width - self.graphical_width) * 7 // 8
        self.controls_graphical_y: int = 310
        self.play_graphical_x: int = (self.screen_width - self.graphical_width) * 3 // 8
        self.play_graphical_y = 200
        self.rules_graphical_x: int = (self.screen_width - self.graphical_width) // 8
        self.rules_graphical_y = 390
        self.rules_exit_graphical_x: int = (self.screen_width - self.graphical_width) // 2
        self.rules_exit_graphical_y = 520
        self.exit_graphical_x: int = (self.screen_width - self.graphical_width) * 5 // 8
        self.exit_graphical_y = 500
        self.setup_graphical_x: int = (self.screen_width - self.graphical_width) // 2
        self.setup_graphical_y: int = 320

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

        color: tuple = (20, 20, 72)  # Цвет текста
        smoothing: bool = True  # Нужно ли сглаживать текст
        text = self.font.render(text_str, smoothing, color)  # Объект текста
        self.game.graphic_engine.screen.blit(text, (graphical_x, graphical_y))

    def print_text_title(self, text_str: str, graphical_x: int, graphical_y: int):
        """
        Печатает текст

        text_str - текст, который нужно напечатать
        graphical_x - графическая координата x текста в [px]
        graphical_y - графическая координата y текста в [px]
        """

        color: tuple = (20, 20, 72)  # Цвет текста
        smoothing: bool = True  # Нужно ли сглаживать текст
        text = self.font_title.render(text_str, smoothing, color)  # Объект текста
        self.game.graphic_engine.screen.blit(text, (graphical_x, graphical_y))

    # --- Логика ---
    def switch_to_controls(self):
        """
        Показывает управление
        """

        self.status: str = 'controls'  # Показать управление

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
        self.print_text_title('Forest Survival', self.game.graphic_engine.screen_width * 3 // 8, 30)

    def manage_logic(self):
        """
        Обрабатывает логические события меню

        screen - экран Pygame
        """

        # Переобозначения
        control_gr_x = self.controls_graphical_x
        control_gr_y = self.controls_graphical_y
        rules_exit_gr_x = self.rules_exit_graphical_x
        rules_exit_gr_y = self.rules_exit_graphical_y
        setup_gr_x = self.setup_graphical_x
        setup_gr_y = self.setup_graphical_y

        if self.status == 'main':  # Если игрок в главном меню
            self.button_controls.process()
            self.button_play.process()
            self.button_rules.process()
            self.button_exit.process()
            self.print_text('Управление', control_gr_x + self.text_x, control_gr_y + self.text_y)
            self.print_text('Играть', self.play_graphical_x + self.text_x, self.play_graphical_y + self.text_y)
            self.print_text('Правила', self.rules_graphical_x + self.text_x, self.rules_graphical_y + self.text_y)
            self.print_text('Выход', self.exit_graphical_x + self.text_x, self.exit_graphical_y + self.text_y)
        elif self.status == 'controls':  # Если игрок смотрит управление
            self.button_rules_exit.process()
            self.print_text('Меню', rules_exit_gr_x + self.text_x, rules_exit_gr_y + self.text_y)
            self.print_text('W, A, S, D - перемещение', 20, 140)
            self.print_text('E - действие: подобрать предмет, обыскать дом, растопить снег', 20, 200)
            self.print_text('I - открыть инвентарь', 20, 260)
            self.print_text('Esc - выйти в меню, выйти из инвентаря', 20, 320)
        elif self.status == 'rules':  # Если игрок читает правила
            self.print_text('Правила', 20, 60)
            self.print_text('1) Чтобы не погибнуть от голода, найдите еду в лесу и съешьте её.', 20, 120)
            self.print_text('2) Чтобы не погибнуть от жажды разведите кострёр, растопите снег', 20, 180)
            self.print_text('и выпейте воду.', 20, 220)
            self.print_text('3) Чтобы развести костёр, вам нужно найти 5 палок в лесу, одну спичку', 20, 280)
            self.print_text('и один лист бумагив доме. Помните, спички и бумага в домах ', 20, 320)
            self.print_text('генерируются случайным образом.', 20, 360)
            self.print_text('4) Для победы вам нужно найти деревню и зайти в неё.', 20, 420)
            self.button_rules_exit.process()
            self.print_text('Меню', rules_exit_gr_x + self.text_x, rules_exit_gr_y + self.text_y)
        elif self.status == 'frost':  # Если герой погиб от переохлаждения
            self.button_setup.process()
            self.print_text('Вы погибли от переохлаждения', 20, 200)
            self.print_text('Лучше бы матан ботали!', 20, 250)
            self.print_text('Вернуться в меню', setup_gr_x + self.text_x, setup_gr_y + self.text_y)
        elif self.status == 'thirst':  # Если герой погиб от жажды
            self.button_setup.process()
            self.print_text('Вы погибли от жажды', 20, 200)
            self.print_text('Лучше бы матан ботали!', 20, 250)
            self.print_text('Вернуться в меню', setup_gr_x + self.text_x, setup_gr_y + self.text_y)
        elif self.status == 'starvation':  # Если герой погиб от голода
            self.button_setup.process()
            self.print_text('Вы погибли от голода', 20, 200)
            self.print_text('Лучше бы матан ботали!', 20, 250)
            self.print_text('Вернуться в меню', setup_gr_x + self.text_x, setup_gr_y + self.text_y)
        elif self.status == 'village':  # Если герой нашёл деревню
            self.button_setup.process()
            self.print_text('Вы нашли деревню, поздравляем с победой!', 20, 200)
            self.print_text('А теперь пора ботать матан!', 20, 250)
            self.print_text('Вернуться в меню', setup_gr_x + self.text_x, setup_gr_y + self.text_y)
