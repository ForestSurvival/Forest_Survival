"""
Модуль инвентаря
"""

from pygame.font import *

from apple import Apple
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

        # Логика
        self.apples_amount: int = 0  # В начале инвентарь пуст

        # Графика
        self.apple_x: int = 5  # Координата x запси о яблоке в [px]
        self.apple_y: int = 40  # Координата y записи о яблоке в [px]
        self.screen = hero.game.screen

        # Текст
        self.font = None  # Шрифт определяется в inventory.setup()
        self.font_smoothing: bool = True  # Сглаживание шрифта
        self.text_color: tuple = (79, 70, 202)  # Цвет текста
        self.text_space = 10  # Ширина пробела между изображением объекта и записью о количестве его копий в [px]

        # Объекты
        self.apple = Apple(hero.game.forest, 0, 0)  # Объект яблока
        self.button_apple = Button(hero.eat_apple, self, self.apple_x, self.apple_y)  # Объект кнопки яблока
        self.hero = hero  # Объект героя

    # --- Логика ---
    def setup(self):
        """
        Инициализация инвентаря
        """

        self.set_font()

    # --- Графика ---
    def print_amount(self, item, amount: int, y: int):
        """
        Печатает количество объектов

        item - объект, количество копий которого надо напечатать
        amount - количество копий объекта
        y - координата y записи об объекте в [px]
        """

        text_x: int = self.apple_x + item.radius + self.text_space  # Координата x названия в [px]
        amount_str: str = str(amount)  # Количество копий объекта
        text = self.font.render(amount_str, self.font_smoothing, self.text_color)  # Текст о количестве копий объекта

        self.screen.blit(text, (text_x, y))

    def show(self):
        """
        Показывает инвентарь
        """

        self.show_apple()

    def set_font(self):
        """
        Устанавливает шрифт
        """

        font_name = None  # Имя шрифта
        font_size: int = 30  # Размер шрифта
        self.font = Font(font_name, font_size)  # Шрифт Pygame

    def show_apple(self):
        """
        Показывает информацию о яблоках
        """

        self.apple.draw(self.apple_x, self.apple_y)
        self.print_amount(self.apple, self.apples_amount, self.apple_y)

    # --- Обработка ---

    def process(self):
        """
        Обрабатывает события инвентаря
        """

        self.button_apple.process()
        self.show()
