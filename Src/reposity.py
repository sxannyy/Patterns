""" Репозиторий данных, хранящий в себе различные ключи всех данных сущностей """

class reposity:
    __data = {}

    @property
    def data(self):
        return self.__data
    
    # Ключ для единиц измерений
    @staticmethod
    def measure_key():
        return "measures"
    
    # Ключ для рецептов
    @staticmethod
    def recipe_key():
        return "recipes"
    
    # Ключ для номенклатуры
    @staticmethod
    def nomenclature_key():
        return "nomenclature"
    
    # Ключ для групп
    @staticmethod
    def nomenclature_group_key():
        return "nomenclature_groups"
    
    """
    Получить список всех ключей
    Источник: https://github.com/Alyona1619
    """

    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(reposity) if
                    callable(getattr(reposity, method)) and method.endswith('_key')]

        for method in methods:
            key = getattr(reposity, method)()
            result.append(key)
        return result

    """ Инициализация """

    def initalize(self):
        keys = reposity.keys()
        for key in keys:
            self.__data[key] = []