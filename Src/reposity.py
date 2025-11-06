"""
Репозиторий данных для хранения всех сущностей приложения.

Класс предоставляет централизованное хранилище для всех данных приложения
с организацией по типам сущностей через систему ключей.
"""

class reposity:
    # Приватный словарь для хранения всех данных приложения
    __data = {}

    @property
    def data(self):
        """
        Предоставляет доступ к данным репозитория.
        
        Возвращает:
            dict: Словарь со всеми данными приложения, организованными по ключам
        """
        return self.__data
    
    @staticmethod
    def measure_key():
        """
        Ключ для доступа к единицам измерения.
        
        Возвращает:
            str: Ключ для словаря единиц измерения
        """
        return "measures"
    
    @staticmethod
    def recipe_key():
        """
        Ключ для доступа к рецептам.
        
        Возвращает:
            str: Ключ для словаря рецептов
        """
        return "recipes"
    
    @staticmethod
    def nomenclature_key():
        """
        Ключ для доступа к номенклатуре.
        
        Возвращает:
            str: Ключ для словаря номенклатуры продуктов
        """
        return "nomenclature"
    
    @staticmethod
    def nomenclature_group_key():
        """
        Ключ для доступа к группам номенклатуры.
        
        Возвращает:
            str: Ключ для словаря групп номенклатуры
        """
        return "nomenclature_groups"
    
    @staticmethod
    def storage_key():
        """
        Ключ для доступа к складам.
        
        Возвращает:
            str: Ключ для словаря складов
        """
        return "storages"
    
    @staticmethod
    def transaction_key():
        """
        Ключ для доступа к транзакциям.
        
        Возвращает:
            str: Ключ для словаря транзакций
        """
        return "transactions"

    @staticmethod
    def keys() -> list:
        """
        Возвращает список всех доступных ключей репозитория.
        
        Использует рефлексию для автоматического поиска всех методов,
        заканчивающихся на '_key'.
        
        Возвращает:
            list: Список всех ключей репозитория
        """
        result = []
        # Находим все методы класса, которые заканчиваются на '_key'
        methods = [method for method in dir(reposity) if
                    callable(getattr(reposity, method)) and method.endswith('_key')]

        # Вызываем каждый метод для получения значения ключа
        for method in methods:
            key = getattr(reposity, method)()
            result.append(key)
        return result

    def initalize(self):
        """
        Инициализирует структуру данных репозитория.
        
        Создает пустые словари для каждого типа сущностей
        на основе всех доступных ключей.
        """
        # Получаем все ключи репозитория
        keys = reposity.keys()
        
        # Инициализируем пустые словари для каждого ключа
        for key in keys:
            self.__data[key] = {}