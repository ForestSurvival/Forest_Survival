"""
Модуль инвентаря
"""

from pygame.font import *

from button import Button


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

        # Графика
        self.apple_graphical_x: int = 5  # Графическая координата x запси о яблоке в [px]
        self.apple_graphical_y: int = 40  # Графическая координата y записи о яблоке в [px]
        self.match_graphical_x: int = 200  # Графическая координата x запси о спичке в [px]
        self.match_graphical_y: int = 40  # Графическая координата y запси о спичке в [px]
        self.paper_graphical_x: int = 200  # Графическая координата x запси о бумаге в [px]
        self.paper_graphical_y: int = 80  # Графическая координата y запси о бумаге в [px]
        self.stick_graphical_x: int = 200  # Графическая коордиата x записи о палке в [px]
        self.stick_graphical_y: int = 120  # Графическая координата y записи о палке в [px]

        # Текст
        self.font = None  # Шрифт определяется в inventory.setup()
        self.font_smoothing: bool = True  # Сглаживание шрифта
        self.text_color: tuple = (79, 70, 202)  # Цвет текста
        self.text_space = 10  # Ширина пробела между изображением объекта и записью о количестве его копий в [px]

        # Объекты
        self.apple = None  # Объект яблока определяется в inventory.setup()

        # Объект кнопки яблока
        self.button_apple = Button(hero.eat_apple, self, self.apple_graphical_x, self.apple_graphical_y)

        self.hero = hero  # Объект героя
        self.match = None  # Объект спички определяется в inventory.setup()
        self.paper = None  # Объект бумаги определяется в inventory.setup()
        self.stick = None  # Объект палки определяется в inventory.setup()

    # --- Инициализация ---
    def get_apple(self):
        """
        Определяет объект яблока
        """

        self.apple = self.hero.game.forest.apples_list[0]  # Объект яблока

    def get_match(self):
        """
        Определяет объект спички
        """

        self.match = self.hero.game.forest.houses_list[0].match  # Объект спички

    def get_paper(self):
        """
        Определяет объект бумаги
        """

        self.paper = self.hero.game.forest.houses_list[0].paper  # Объект бумаги

    def get_stick(self):
        """
        Определяет объект палки
        """

        self.stick = self.hero.game.forest.sticks_list[0]  # Обект палки

    def set_font(self):
        """
        Устанавливает шрифт
        """

        font_name = None  # Имя шрифта
        font_size: int = 30  # Размер шрифта
        self.font = Font(font_name, font_size)  # Шрифт Pygame

    def setup(self):
        """
        Инициализация инвентаря
        """

        self.get_apple()
        self.set_font()
        self.get_match()
        self.get_paper()
        self.get_stick()

    # --- Графика ---
    def print_amount(self, item, amount: int, graphical_x: int, graphical_y: int):
        """
        Печатает количество объектов

        item - объект, количество копий которого надо напечатать
        amount - количество копий объекта
        graphical_x - графическая координата x записи об объекте в [px]
        graphical_y - графическая координата y записи об объекте в [px]
        """

        # Графическая координата x текста в [px]
        text_graphical_x: int = graphical_x + item.radius + self.text_space

        amount_str: str = str(amount)  # Количество копий объекта
        text = self.font.render(amount_str, self.font_smoothing, self.text_color)  # Текст о количестве копий объекта

        self.hero.game.screen.blit(text, (text_graphical_x, graphical_y))

    def show_apple(self):
        """
        Показывает информацию о яблоках
        """

        self.apple.draw(self.apple_graphical_x, self.apple_graphical_y)
        self.print_amount(self.apple, self.apples_amount, self.apple_graphical_x, self.apple_graphical_y)

    def show_match(self):
        """
        Показывает информацию о спичках
        """

        self.match.draw(self.match_graphical_x, self.match_graphical_y)
        self.print_amount(self.match, self.matches_amount, self.match_graphical_x, self.match_graphical_y)

    def show_paper(self):
        """
        Показывает информацию о бумаге
        """

        self.paper.draw(self.paper_graphical_x, self.paper_graphical_y)
        self.print_amount(self.paper, self.paper_amount, self.paper_graphical_x, self.paper_graphical_y)

    def show_stick(self):
        """
        Показывает информацию о палках
        """

        self.stick.draw(self.stick_graphical_x, self.stick_graphical_y)
        self.print_amount(self.stick, self.sticks_amount, self.stick_graphical_x, self.stick_graphical_y)

    # --- Обработка ---
    def manage_graphics(self):
        """
        Обабатывает графические события инвентаря
        """

        self.show_apple()
        self.show_match()
        self.show_paper()
        self.show_stick()

    def process(self):
        """
        Обрабатывает события инвентаря
        """

        self.button_apple.process()
        self.manage_graphics()
