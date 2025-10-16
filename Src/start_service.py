from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.reposity import reposity
from Src.Models.measure_model import measure_model
from Src.Models.recipe_model import recipe_model

"""
    Класс для инициализации и управления репозиторием данных кулинарного приложения.

    Этот класс реализует Singleton и отвечает за создание начальных данных,
    таких как единицы измерения, группы номенклатуры и сами ингредиенты. Он
    взаимодействует с репозиторием для хранения и извлечения информации о
    кулинарных ингредиентах и рецептах.

    Атрибуты:
        repo (reposity): Репозиторий, содержащий данные о единицах измерения,
                         номенклатуре и группах номенклатуры.

    Методы:
        __init(): Инициализирует репозиторий с пустыми данными.
        __new(cls): Реализует паттерн Singleton для класса start_service.
        __default_create_measure(): Создает стандартные единицы измерения.
        __default_create_nomenclature(): Создает стандартные ингредиенты.
        __default_create_nomenclature_group(): Создает стандартные группы
            номенклатуры.
        data(): Возвращает данные.
        __default_create_recipe_waffles(): Создает рецепт вафель с заданными шагами и ингредиентами.
        start(): Инициализирует эталонные данные, создавая единицы измерения, группы номенклатуры, ингредиенты и рецепт вафель.
"""


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
        self.__repo.data[reposity.nomenclature_group_key]['СиП'] = (nomenclature_group_model.create("специи и пряности"))
        self.__repo.data[reposity.nomenclature_group_key]['ЖПП'] = (nomenclature_group_model.create("продукты животного происхождения"))
        self.__repo.data[reposity.nomenclature_group_key]['МиК'] = (nomenclature_group_model.create("мука и крупы"))

    """
    Стартовый набор данных
    """
    def data(self):
        return self.__repo.data   
    
    """ Дефолтный рецепт вафель """
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

        recipe = recipe_model.create("Вафли", steps, ingredients)
        self.repo.data[reposity.recipe_key]['Вафли'] = recipe
        return recipe
    
    """ Дефолтный рецепт омлета """
    def __create_omelette_recipe(self):
        steps = [
            'Подготовка яиц: Яйца куриные достаньте заранее, чтобы они достигли комнатной температуры',
            'Взбивание основы: В миске взбейте яйца с солью и черным перцем до легкой пены и однородной консистенции',
            'Добавление молока: Постепенно влейте молоко, аккуратно перемешивая. Избегайте интенсивного взбивания',
            'Подготовка сковороды: В сковороде растопите сливочное масло, равномерно распределите по всей поверхности',
            'Выпекание: Вылейте яично-молочную смесь в разогретую сковороду. Накройте крышкой',
            'Приготовление: Готовьте на среднем огне 7-10 минут. Омлет готов, когда края золотятся, а середина пропечена',
            'Подача: Немного дайте омлету остыть в сковороде, затем аккуратно сверните или разрежьте на порции. Подавайте сразу после приготовления'        
        ]
        nomenclature = self.__repo.data[reposity.nomenclature_key]

        ingredients = [
            tuple([nomenclature['Яйца куриные'], 3]),
            tuple([nomenclature['Молоко'], 150]),
            tuple([nomenclature['Соль'], 3]),
            tuple([nomenclature['Сливочное масло'], 20]),
            tuple([nomenclature['Перец черный'], 2]),
        ]

        recipe = recipe_model.create("Омлет с молоком", steps, ingredients)
        self.repo.data[reposity.recipe_key]['Омлет с молоком'] = recipe
        return recipe
    
    """ Дефолтный рецепт лепешек """
    def __create_flatjack_recipe(self):
        steps = [
            'Подготовка ингредиентов: В миске взбейте яйца куриные с солью до однородности',
            'Смешивание жидкой основы: Добавьте молоко и растопленное сливочное масло, тщательно перемешайте',
            'Замес теста: Постепенно всыпайте пшеничную муку через сито, постоянно помешивая. Сначала используйте венчик, затем вымешивайте руками',
            'Отдых теста: Замесите крутое эластичное тесто, накройте полотенцем и оставьте отдыхать 15 минут при комнатной температуре',
            'Формирование лепешек: Разделите тесто на 6 равных частей. Каждую часть раскатайте в тонкую круглую лепешку толщиной 3-4 мм',
            'Выпекание: Разогрейте сухую сковороду на среднем огне. Обжаривайте лепешки по 2-3 минуты с каждой стороны до появления золотистых пятен',
            'Подача: Готовые лепешки смажьте сливочным маслом. Готово!'        
        ]
        nomenclature = self.__repo.data[reposity.nomenclature_key]

        ingredients = [
            tuple([nomenclature['Пшеничная мука'], 400]),
            tuple([nomenclature['Яйца куриные'], 2]),
            tuple([nomenclature['Молоко'], 200]),
            tuple([nomenclature['Соль'], 5]),
            tuple([nomenclature['Сливочное масло'], 30]),
        ]

        recipe = recipe_model.create("Простые лепешки", steps, ingredients)
        self.repo.data[reposity.recipe_key]['Простые лепешки'] = recipe
        return recipe
       

    """
    Основной метод для генерации эталонных данных
    """
    def start(self):
        self.__default_create_measure()
        self.__default_create_nomenclature_group()
        self.__default_create_nomenclature()
        self.__default_create_recipe_waffles()
        self.__create_omelette_recipe()
        self.__create_flatjack_recipe()
        
