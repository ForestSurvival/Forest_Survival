"""
Модуль инвентаря
"""


class Inventory(object):
    """
    Описывает инвентарь
    """

    def __init__(self):
        """
        Параметры
        """

        self.apples_amount: int = 0  # В начале инвентарь пуст

    # --- Обработка ---
    def log(self):
        """
        Выводит данные в консоль для отладки
        """

        print('Hero inventory apples amount:', self.apples_amount)
        print('--- Game cycle ---')

    def process(self):
        """
        Обрабатывает события инвентаря
        """

        # Отладка
        # self.log()
