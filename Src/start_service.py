from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.reposity import reposity
from Src.Models.measure_model import measure_model
from Src.Models.recipe_model import recipe_model

class start_service:
    __repo: reposity = reposity()

    def __init__(self):
        self.__repo.data[reposity.measure_key] = {}
        self.__repo.data[reposity.nomenclature_key] = {}
        self.__repo.data[reposity.nomenclature_group_key] = {}
        self.__repo.data[reposity.recipe_key] = {}

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance 
    
    @property
    def repo(self):
        return self.__repo

    def __default_create_measure(self):
        self.__repo.data[reposity.measure_key]['г'] = (measure_model.create_gramm())
        self.__repo.data[reposity.measure_key]['кг'] = (measure_model.create_kilogramm())
        self.__repo.data[reposity.measure_key]['л'] = (measure_model.create_liter())
        self.__repo.data[reposity.measure_key]['мл'] = (measure_model.create_milliliter())
        self.__repo.data[reposity.measure_key]['шт'] = (measure_model.create_piece())

    def __default_create_nomenclature(self):
        self.__repo.data[reposity.nomenclature_key]['Сахар'] = nomenclature_model(
            'Сахар', 'Сахар', 
            self.__repo.data[reposity.nomenclature_group_key]['СиП'],
            self.__repo.data[reposity.measure_key]['г']
        )

        self.__repo.data[reposity.nomenclature_key]['Пшеничная мука'] = nomenclature_model(
        'Пшеничная мука', 'Мука пшеничная', 
        self.__repo.data[reposity.nomenclature_group_key]['МиК'],
        self.__repo.data[reposity.measure_key]['г']
    )
        
        self.__repo.data[reposity.nomenclature_key]['Сливочное масло'] = nomenclature_model(
        'Сливочное масло', 'Масло сливочное', 
        self.__repo.data[reposity.nomenclature_group_key]['ЖПП'],
        self.__repo.data[reposity.measure_key]['г']
    )
        
        self.__repo.data[reposity.nomenclature_key]['Яйца куриные'] = nomenclature_model(
        'Яйца куриные', 'Яйцо куриное', 
        self.__repo.data[reposity.nomenclature_group_key]['ЖПП'],
        self.__repo.data[reposity.measure_key]['шт']
    )
        
        self.__repo.data[reposity.nomenclature_key]['Ванилин'] = nomenclature_model(
        'Ванилин', 'Ванилин', 
        self.__repo.data[reposity.nomenclature_group_key]['СиП'],
        self.__repo.data[reposity.measure_key]['г']
    )
        
        self.__repo.data[reposity.nomenclature_key]['Соль'] = nomenclature_model(
        'Соль', 'Соль поваренная', 
        self.__repo.data[reposity.nomenclature_group_key]['СиП'],
        self.__repo.data[reposity.measure_key]['г']
    )
    
        self.__repo.data[reposity.nomenclature_key]['Перец черный'] = nomenclature_model(
        'Перец черный', 'Перец черный молотый', 
        self.__repo.data[reposity.nomenclature_group_key]['СиП'],
        self.__repo.data[reposity.measure_key]['г']
    )
    
        self.__repo.data[reposity.nomenclature_key]['Молоко'] = nomenclature_model(
        'Молоко', 'Молоко коровье', 
        self.__repo.data[reposity.nomenclature_group_key]['ЖПП'],
        self.__repo.data[reposity.measure_key]['мл']
    )

    def __default_create_nomenclature_group(self):
        self.__repo.data[reposity.nomenclature_group_key]['СиП'] = (nomenclature_group_model.create_spices_and_herbs())
        self.__repo.data[reposity.nomenclature_group_key]['ЖПП'] = (nomenclature_group_model.create_animal_products())
        self.__repo.data[reposity.nomenclature_group_key]['МиК'] = (nomenclature_group_model.create_flour_and_cereals())

    """
    Стартовый набор данных
    """
    def data(self):
        return self.__repo.data   
    
    """
    """
    def __default_create_recipe_waffles(self):
        steps = [
            'Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см.',
            'Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.',
            'Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.',
            'Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.',
            'Всыпьте муку, добавьте ванилин.',
            'Перемешайте массу венчиком до состояния гладкого однородного теста.',
            'Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно! Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке. Можно класть немного меньше теста, тогда вафли будут меньше и их получится больше.',
            'Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик.'
        ]
        nomenclature = self.__repo.data[reposity.nomenclature_key]

        ingredients = [
            tuple([nomenclature['Пшеничная мука'], 100]),
            tuple([nomenclature['Сахар'], 80]),
            tuple([nomenclature['Сливочное масло'], 70]),
            tuple([nomenclature['Яйца куриные'], 1]),
            tuple([nomenclature['Ванилин'], 5])
        ]

        return recipe_model.create("Вафли", steps, ingredients)

    """
    Основной метод для генерации эталонных данных
    """
    def start(self):
        self.__default_create_measure()
        self.__default_create_nomenclature_group()
        self.__default_create_nomenclature()
        self.__default_create_recipe_waffles()
        
