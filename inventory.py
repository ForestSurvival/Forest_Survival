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
        self.sticks_amount: int = 0  # Количество палок

        # Графика
        self.apple_graphical_x: int = 5  # Координата x запси о яблоке в [px]
        self.apple_graphical_y: int = 40  # Координата y записи о яблоке в [px]
        self.stick_graphical_x: int = 200  # Графическая коордиата x записи о палке в [px]
        self.stick_graphical_y: int = 40  # Графическая координата y записи о палке в [px]

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
        self.stick = None  # Объект палки определяется в inventory.setup()

    # --- Инициализация ---
    def get_apple(self):
        """
        Определяет объект яблока
        """

        self.apple = self.hero.game.forest.apples_list[0]  # Объект яблока

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
        self.get_stick()
        self.set_font()

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
        self.show_stick()

    def process(self):
        """
        Обрабатывает события инвентаря
        """

        self.button_apple.process()
        self.manage_graphics()
