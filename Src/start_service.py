from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.reposity import reposity
from Src.Models.measure_model import measure_model
from Src.Models.recipe_model import recipe_model

"""
    Сервис инициализации и управления данными кулинарного приложения.

    Класс реализует паттерн Singleton и отвечает за:
    - Создание и наполнение репозитория стартовыми данными
    - Инициализацию справочников (единицы измерения, группы продуктов)
    - Генерацию тестовых рецептов и ингредиентов
    - Предоставление доступа к данным через репозиторий

    Основные функциональные блоки:
    1. Инициализация структур данных репозитория
    2. Создание эталонных единиц измерения (граммы, литры, штуки и т.д.)
    3. Формирование групп номенклатуры (специи, продукты животного происхождения, мука и крупы)
    4. Генерация базовых ингредиентов (сахар, мука, яйца, масло и др.)
    5. Создание демонстрационных рецептов (вафли, омлет, лепешки)

    Атрибуты:
        __repo (reposity): Центральный репозиторий для хранения всех данных приложения

    Методы:
        __init__(): Инициализирует структуры данных репозитория
        __new__(): Реализует паттерн Singleton
        start(): Основной метод инициализации всех справочников и рецептов
"""


class start_service:
    __repo: reposity = reposity()

    def __init__(self):
        """
        Инициализация структур данных репозитория.
        
        Создает пустые словари для хранения:
        - Единиц измерения (measure_key)
        - Номенклатуры продуктов (nomenclature_key) 
        - Групп номенклатуры (nomenclature_group_key)
        - Рецептов (recipe_key)
        """
        self.__repo.data[reposity.measure_key()] = {}
        self.__repo.data[reposity.nomenclature_key()] = {}
        self.__repo.data[reposity.nomenclature_group_key()] = {}
        self.__repo.data[reposity.recipe_key()] = {}

    # Реализация паттерна Singleton
    def __new__(cls):
        """
        Реализация паттерна Singleton.
        
        Обеспечивает создание только одного экземпляра класса
        во время работы приложения.
        
        Returns:
            start_service: Единственный экземпляр класса
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance 
    
    @property
    def repo(self):
        """
        Предоставляет доступ к репозиторию данных.
        
        Returns:
            reposity: Репозиторий со всеми данными приложения
        """
        return self.__repo

    def __default_create_measure(self):
        """
        Создает стандартные единицы измерения.
        
        Добавляет в репозиторий базовые единицы измерения:
        - Граммы (г)
        - Килограммы (кг) 
        - Литр (л)
        - Миллилитры (мл)
        - Штуки (шт)
        """
        self.__repo.data[reposity.measure_key()]['г'] = (measure_model.create_gramm())
        self.__repo.data[reposity.measure_key()]['кг'] = (measure_model.create_kilogramm())
        self.__repo.data[reposity.measure_key()]['л'] = (measure_model.create_liter())
        self.__repo.data[reposity.measure_key()]['мл'] = (measure_model.create_milliliter())
        self.__repo.data[reposity.measure_key()]['шт'] = (measure_model.create_piece())

    def __default_create_nomenclature(self):
        """
        Создает стандартные ингредиенты для рецептов.
        
        Генерирует базовый набор продуктов с привязкой к группам номенклатуры
        и единицам измерения:
        - Сахар, соль, ванилин, перец (группа специй, единица - граммы)
        - Мука пшеничная (группа муки и круп, единица - граммы)
        - Яйца, молоко, масло (группа животных продуктов, единицы - граммы/мл/шт)
        """
        self.__repo.data[reposity.nomenclature_key()]['Сахар'] = nomenclature_model(
            'Сахар', 'Сахар', 
            self.__repo.data[reposity.nomenclature_group_key()]['СиП'],
            self.__repo.data[reposity.measure_key()]['г']
        )

        self.__repo.data[reposity.nomenclature_key()]['Пшеничная мука'] = nomenclature_model(
        'Пшеничная мука', 'Мука пшеничная', 
        self.__repo.data[reposity.nomenclature_group_key()]['МиК'],
        self.__repo.data[reposity.measure_key()]['г']
    )
        
        self.__repo.data[reposity.nomenclature_key()]['Сливочное масло'] = nomenclature_model(
        'Сливочное масло', 'Масло сливочное', 
        self.__repo.data[reposity.nomenclature_group_key()]['ЖПП'],
        self.__repo.data[reposity.measure_key()]['г']
    )
        
        self.__repo.data[reposity.nomenclature_key()]['Яйца куриные'] = nomenclature_model(
        'Яйца куриные', 'Яйцо куриное', 
        self.__repo.data[reposity.nomenclature_group_key()]['ЖПП'],
        self.__repo.data[reposity.measure_key()]['шт']
    )
        
        self.__repo.data[reposity.nomenclature_key()]['Ванилин'] = nomenclature_model(
        'Ванилин', 'Ванилин', 
        self.__repo.data[reposity.nomenclature_group_key()]['СиП'],
        self.__repo.data[reposity.measure_key()]['г']
    )
        
        self.__repo.data[reposity.nomenclature_key()]['Соль'] = nomenclature_model(
        'Соль', 'Соль поваренная', 
        self.__repo.data[reposity.nomenclature_group_key()]['СиП'],
        self.__repo.data[reposity.measure_key()]['г']
    )
    
        self.__repo.data[reposity.nomenclature_key()]['Перец черный'] = nomenclature_model(
        'Перец черный', 'Перец черный молотый', 
        self.__repo.data[reposity.nomenclature_group_key()]['СиП'],
        self.__repo.data[reposity.measure_key()]['г']
    )
    
        self.__repo.data[reposity.nomenclature_key()]['Молоко'] = nomenclature_model(
        'Молоко', 'Молоко коровье', 
        self.__repo.data[reposity.nomenclature_group_key()]['ЖПП'],
        self.__repo.data[reposity.measure_key()]['мл']
    )

    def __default_create_nomenclature_group(self):
        """
        Создает стандартные группы номенклатуры.
        
        Формирует категории для классификации ингредиентов:
        - СиП: Специи и пряности
        - ЖПП: Продукты животного происхождения  
        - МиК: Мука и крупы
        """
        self.__repo.data[reposity.nomenclature_group_key()]['СиП'] = (nomenclature_group_model.create("специи и пряности"))
        self.__repo.data[reposity.nomenclature_group_key()]['ЖПП'] = (nomenclature_group_model.create("продукты животного происхождения"))
        self.__repo.data[reposity.nomenclature_group_key()]['МиК'] = (nomenclature_group_model.create("мука и крупы"))

    def data(self):
        """
        Предоставляет доступ ко всем данным репозитория.
        
        Returns:
            dict: Словарь со всеми данными приложения
        """
        return self.__repo.data   
    
    def __default_create_recipe_waffles(self):
        """
        Создает рецепт вафель.
        
        Формирует полный рецепт с пошаговой инструкцией и списком ингредиентов.
        Включает все этапы приготовления от подготовки продуктов до выпекания.
        
        Returns:
            recipe_model: Объект рецепта вафель
        """
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
        nomenclature = self.__repo.data[reposity.nomenclature_key()]

        ingredients = [
            tuple([nomenclature['Пшеничная мука'], 100]),
            tuple([nomenclature['Сахар'], 80]),
            tuple([nomenclature['Сливочное масло'], 70]),
            tuple([nomenclature['Яйца куриные'], 1]),
            tuple([nomenclature['Ванилин'], 5])
        ]

        recipe = recipe_model.create("Вафли", steps, ingredients)
        self.repo.data[reposity.recipe_key()]['Вафли'] = recipe
        return recipe
    
    def __create_omelette_recipe(self):
        """
        Создает рецепт омлета с молоком.
        
        Формирует классический рецепт омлета с подробными шагами приготовления
        и точными пропорциями ингредиентов.
        
        Returns:
            recipe_model: Объект рецепта омлета
        """
        steps = [
            'Подготовка яиц: Яйца куриные достаньте заранее, чтобы они достигли комнатной температуры',
            'Взбивание основы: В миске взбейте яйца с солью и черным перцем до легкой пены и однородной консистенции',
            'Добавление молока: Постепенно влейте молоко, аккуратно перемешивая. Избегайте интенсивного взбивания',
            'Подготовка сковороды: В сковороде растопите сливочное масло, равномерно распределите по всей поверхности',
            'Выпекание: Вылейте яично-молочную смесь в разогретую сковороду. Накройте крышкой',
            'Приготовление: Готовьте на среднем огне 7-10 минут. Омлет готов, когда края золотятся, а середина пропечена',
            'Подача: Немного дайте омлету остыть в сковороде, затем аккуратно сверните или разрежьте на порции. Подавайте сразу после приготовления'        
        ]
        nomenclature = self.__repo.data[reposity.nomenclature_key()]

        ingredients = [
            tuple([nomenclature['Яйца куриные'], 3]),
            tuple([nomenclature['Молоко'], 150]),
            tuple([nomenclature['Соль'], 3]),
            tuple([nomenclature['Сливочное масло'], 20]),
            tuple([nomenclature['Перец черный'], 2]),
        ]

        recipe = recipe_model.create("Омлет с молоком", steps, ingredients)
        self.repo.data[reposity.recipe_key()]['Омлет с молоком'] = recipe
        return recipe
    
    def __create_flatjack_recipe(self):
        """
        Создает рецепт простых лепешек.
        
        Формирует рецепт домашних лепешек с пошаговым описанием процесса
        от замеса теста до выпекания на сковороде.
        
        Returns:
            recipe_model: Объект рецепта лепешек
        """
        steps = [
            'Подготовка ингредиентов: В миске взбейте яйца куриные с солью до однородности',
            'Смешивание жидкой основы: Добавьте молоко и растопленное сливочное масло, тщательно перемешайте',
            'Замес теста: Постепенно всыпайте пшеничную муку через сито, постоянно помешивая. Сначала используйте венчик, затем вымешивайте руками',
            'Отдых теста: Замесите крутое эластичное тесто, накройте полотенцем и оставьте отдыхать 15 минут при комнатной температуре',
            'Формирование лепешек: Разделите тесто на 6 равных частей. Каждую часть раскатайте в тонкую круглую лепешку толщиной 3-4 мм',
            'Выпекание: Разогрейте сухую сковороду на среднем огне. Обжаривайте лепешки по 2-3 минуты с каждой стороны до появления золотистых пятен',
            'Подача: Готовые лепешки смажьте сливочным маслом. Готово!'        
        ]
        nomenclature = self.__repo.data[reposity.nomenclature_key()]

        ingredients = [
            tuple([nomenclature['Пшеничная мука'], 400]),
            tuple([nomenclature['Яйца куриные'], 2]),
            tuple([nomenclature['Молоко'], 200]),
            tuple([nomenclature['Соль'], 5]),
            tuple([nomenclature['Сливочное масло'], 30]),
        ]

        recipe = recipe_model.create("Простые лепешки", steps, ingredients)
        self.repo.data[reposity.recipe_key()]['Простые лепешки'] = recipe
        return recipe
       

    def start(self):
        """
        Основной метод инициализации всех данных приложения.
        
        Последовательно выполняет создание:
        1. Единиц измерения
        2. Групп номенклатуры
        3. Ингредиентов
        4. Демонстрационных рецептов
        
        Этот метод должен вызываться при старте приложения для наполнения
        репозитория начальными данными.
        """
        self.__default_create_measure()
        self.__default_create_nomenclature_group()
        self.__default_create_nomenclature()
        self.__default_create_recipe_waffles()
        self.__create_omelette_recipe()
        self.__create_flatjack_recipe()