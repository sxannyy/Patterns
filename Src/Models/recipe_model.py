from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model
from Src.Models import nomenclature_model

class empty_list_exception(Exception):
    pass

class recipe_model(abstract_model):
    __ingredients:list = []
    __steps:list = []
    _instances = {}

    def __init__(self, name = ""):
        super().__init__(name)

    @property
    def ingredients(self):
        return self.__ingredients
        
    @ingredients.setter
    def ingredients(self, ingredients:list):
        """  Ингридиенты """
        validator.validate(ingredients, list)
        for i in ingredients:
            validator.validate(i, tuple)
            validator.validate(i[0], nomenclature_model)
            validator.validate(i[1], float|int)
        self.__ingredients = ingredients

    def add_ingredient(self, nomenclature:nomenclature_model, quantity:float|int):
        validator.validate(nomenclature, nomenclature_model)
        validator.validate(quantity, float|int)
        self.__ingridients += tuple(nomenclature,quantity)

    @property
    def steps(self):
        return self.__steps
        
    @steps.setter
    def steps(self, steps:list):
        """ Шаги рецепта """
        validator.validate(steps, list)
        if len(steps) == 0:
            raise empty_list_exception("Пустой массив шагов рецепта!")
        for step in steps:
            validator.validate(step, str, 2000)
        self.__steps = steps

    def add_step(self, step:str):
        validator.validate(step, str, 2000)
        self.__steps.append(step)
    
    @staticmethod
    def create(name:str, steps:list, ingredients:list):
        validator.validate(name, str)
        if name in recipe_model._instances.keys():
            return recipe_model._instances[name]
        validator.validate(steps, list)
        if len(steps) == 0:
            raise empty_list_exception("Пустой массив шагов рецепта!")
        for step in steps:
            validator.validate(step, str, 2000)
        
        validator.validate(ingredients, list)
        for i in ingredients:
            validator.validate(i, tuple)
            validator.validate(i[0], nomenclature_model)
            validator.validate(i[1], float|int)

        item = recipe_model(name)
        item.ingredients = ingredients
        item.steps = steps

        recipe_model._instances[name] = item
        return item