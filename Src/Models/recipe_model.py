from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Dto.recipe_dto import recipe_dto

# Пользовательское исключение для пустого списка
class empty_list_exception(Exception):
    """Исключение, вызываемое при попытке установить пустой список шагов рецепта"""
    pass

class recipe_model(abstract_model):

    """
    Модель рецепта в предметной области.
    Представляет собой рецепт блюда с ингредиентами и пошаговой инструкцией.
    Наследует от abstract_model (поля id, name, unique_code).
    """
    
    # Приватные поля модели
    __ingredients: list = []  # Список ингредиентов: [(nomenclature_model, quantity)]
    __steps: list = []        # Список шагов приготовления: [str]
    _instances = {}           # Кэш экземпляров для паттерна Flyweight

    def __init__(self, name: str = ""):

        """
        Конструктор модели рецепта.
        Аргументы:
            name (str): Название рецепта
        """

        super().__init__(name)

    @property
    def ingredients(self) -> list:
        """Возвращает список ингредиентов рецепта"""
        return self.__ingredients
        
    @ingredients.setter
    def ingredients(self, ingredients: list):

        """
        Устанавливает список ингредиентов с валидацией.
        Аргументы:
            ingredients (list): Список кортежей (nomenclature_model, quantity)
        Проверяет:
            - Тип параметра (должен быть list)
            - Каждый элемент должен быть tuple
            - Первый элемент кортежа должен быть nomenclature_model
            - Второй элемент кортежа должен быть int или float
        """

        validator.validate(ingredients, list)
        for i in ingredients:
            validator.validate(i, tuple)
            validator.validate(i[0], nomenclature_model)
            validator.validate(i[1], float|int)
        self.__ingredients = ingredients

    def add_ingredient(self, nomenclature: nomenclature_model, quantity: float|int):

        """
        Добавляет один ингредиент в рецепт.
        Аргументы:
            nomenclature (nomenclature_model): Модель номенклатуры (ингредиент)
            quantity (float|int): Количество ингредиента
        """

        validator.validate(nomenclature, nomenclature_model)
        validator.validate(quantity, float|int)
        self.__ingredients += [(nomenclature, float(quantity))]

    @property
    def steps(self) -> list:
        """Возвращает список шагов приготовления рецепта"""
        return self.__steps
        
    @steps.setter
    def steps(self, steps: list):

        """
        Устанавливает список шагов рецепта с валидацией.
        Аргументы:
            steps (list): Список строк с шагами приготовления
        Исключения:
            empty_list_exception: Если передан пустой список
        Проверяет:
            - Тип параметра (должен быть list)
            - Список не должен быть пустым
            - Каждый шаг должен быть строкой не длиннее 2000 символов
        """

        validator.validate(steps, list)
        if len(steps) == 0:
            raise empty_list_exception("Пустой массив шагов рецепта!")
        for step in steps:
            validator.validate(step, str, 2000)
        self.__steps = steps

    def add_step(self, step: str):

        """
        Добавляет один шаг в рецепт.
        Аргументы:
            step (str): Текст шага приготовления (макс. 2000 символов)
        """

        validator.validate(step, str, 2000)
        self.__steps.append(step)
    
    @staticmethod
    def create(name: str, steps: list, ingredients: list) -> 'recipe_model':

        """
        Фабричный метод для создания рецепта.
        Аргументы:
            name (str): Название рецепта
            steps (list): Список шагов приготовления
            ingredients (list): Список ингредиентов
        Возвращает:
            recipe_model: Созданный или существующий экземпляр рецепта
        Исключения:
            empty_list_exception: Если передан пустой список шагов
        """

        validator.validate(name, str)
        if name in recipe_model._instances.keys():
            return recipe_model._instances[name]
            
        validator.validate(steps, list)
        if len(steps) == 0:
            raise empty_list_exception("Пустой массив шагов рецепта!")
        for step in steps:
            validator.validate(step, str, 2000)
        
        validator.validate(ingredients, list)

        item = recipe_model(name)
        item.ingredients = ingredients
        item.steps = steps

        # Сохраняем в кэше для повторного использования
        recipe_model._instances[name] = item
        return item

    @staticmethod
    def from_dto(dto: recipe_dto, cache: dict) -> 'recipe_model':

        """
        Создает recipe_model из recipe_dto.
        Аргументы:
            dto (recipe_dto): DTO объект рецепта
            cache (dict): Словарь с кэшированными объектами (nomenclature_model по id)
        Возвращает:
            recipe_model: Созданная модель рецепта
        """

        validator.validate(dto, recipe_dto)
        validator.validate(cache, dict)
        
        # Преобразуем ингредиенты из DTO формата в модель
        ingredients = []
        for ingredient_dto in dto.ingredients:
            nomenclature_id = ingredient_dto.get('nomenclature_id')
            quantity = ingredient_dto.get('quantity', 0)
            
            if nomenclature_id and nomenclature_id in cache:
                nomenclature = cache[nomenclature_id]
                ingredients.append((nomenclature, quantity))
        
        # Создаем модель рецепта
        recipe = recipe_model.create(
            name=dto.name,
            steps=dto.steps,
            ingredients=ingredients
        )
        
        return recipe
    
    def to_dto(self) -> recipe_dto:

        """
        Преобразует recipe_model в recipe_dto
        """

        # Преобразуем ингредиенты в формат для DTO
        ingredients_dto = []
        for ingredient in self.ingredients:
            if len(ingredient) >= 2:
                nomenclature = ingredient[0]
                quantity = ingredient[1]
                ingredients_dto.append({
                    'nomenclature_id': nomenclature.unique_code,
                    'nomenclature_name': nomenclature.name,
                    'quantity': quantity,
                    'measure_unit': nomenclature.measure.name if nomenclature.measure else ''
                })
        
        # Создаем DTO
        dto = recipe_dto()
        dto.id = self.unique_code
        dto.name = self.name
        dto.ingredients = ingredients_dto
        dto.steps = self.steps
        return dto