"""
Модуль логического движка
"""

import pygame


class LogicEngine(object):
    """
    Опиывает логический движок
    """

    def __init__(self, game):
        """
        Параметры

        game - объект игры
        """

        # Логика
        self.keys_amount = None  # Количество клавиш на клавиатуре орпеделяется в logic_engine.setup()
        self.keys_current_list: list = pygame.key.get_pressed()  # Список нажатых в текущем цикле клавиш

        # Список нажатых в предыдущем  цикре клавиш определяется в logic_engine.setup()
        self.keys_latest_list: list = [None]

        self.keys_moment_list: list = [None]  # Список нажатых строго в текущем цикле клавиш
        self.mouse_pos_list: list = [None]  # Список координат клика мыши строго в текущем цикле

        # Объекты
        self.game = game

    # --- Инициализация ---
    def setup(self):
        """
        Инициализация логического движка
        """

        self.count_keys()
        self.set_keys_lists()
    
    # --- Логика ---
    def count_keys(self):
        """
        Считает количество клавиш на клавиатуре
        """

        keys_count_list: list = pygame.key.get_pressed()  # Список нажатых клавиш
        self.keys_amount: int = len(keys_count_list)  # Количество клавиш на клавиатуре

    def manage_logic(self):
        """
        Обрабатывает логические события
        """

        self.keys_current_list = pygame.key.get_pressed()  # Список нажатых в текущем цикле клавиш
        self.mouse_pos_list: list = [None]  # Кнопка мыши не нажата

        for key_index in range(self.keys_amount):

            # Если клавиша нажата строго в текущем цикле
            if self.keys_current_list[key_index] == 1 and self.keys_latest_list[key_index] == 0:
                self.keys_moment_list[key_index]: int = 1  # Занести клавишу в соответствующий список
            else:
                self.keys_moment_list[key_index]: int = 0  # Вычеркнуть клавишу из соответствующего списка
        self.keys_latest_list: list = self.keys_current_list  # Список нажатых в предыдущем цикле клавиш
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # Если совершён клик мышю
                self.mouse_pos_list: list = event.pos  # Список координат клика мыши
            elif event.type == pygame.QUIT:  # Если игрок закрыл окно
                self.game.exit()

    def set_keys_lists(self):
        """
        Заполняет списки клавиш
        """

        self.keys_latest_list: list = [0] * self.keys_amount  # Кнопки не нажаты
        self.keys_moment_list: list = [0] * self.keys_amount  # Кнопки не нажаты

    # --- Обработка ---
    def process(self):
        """
        Обрабатывает события логического движка
        """

        self.manage_logic()
