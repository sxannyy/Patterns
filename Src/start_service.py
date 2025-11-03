from datetime import datetime
from Src.Convertors.convert_factory import convert_factory
from Src.Core.validator import validator
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.osv_model import osv_model
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
from Src.reposity import reposity
from Src.Models.measure_model import measure_model
from Src.Models.recipe_model import recipe_model
from Src.settings_manager import settings_manager
import json
import os

class start_service:
    """
    Сервис инициализации и управления данными кулинарного приложения.

    Класс реализует паттерн Singleton и отвечает за:
    - Создание и наполнение репозитория стартовыми данными
    - Инициализацию справочников (единицы измерения, группы продуктов)
    - Генерацию тестовых рецептов и ингредиентов
    - Предоставление доступа к данным через репозиторий
    - Загрузку и сохранение данных в зависимости от настроек первого старта

    Основные функциональные блоки:
    1. Инициализация структур данных репозитория
    2. Создание эталонных единиц измерения (граммы, литры, штуки и т.д.)
    3. Формирование групп номенклатуры (специи, продукты животного происхождения, мука и крупы)
    4. Генерация базовых ингредиентов (сахар, мука, яйца, масло и др.)
    5. Создание демонстрационных рецептов (вафли, омлет, лепешки)
    6. Управление первым запуском приложения

    Атрибуты:
        __repo (reposity): Центральный репозиторий для хранения всех данных приложения
        __data_file (str): Имя файла для сохранения/загрузки данных
    """

    __repo: reposity = reposity()
    __data_file: str = "app_data.json"

    def __init__(self):
        """
        Инициализация структур данных репозитория.
        
        Создает пустые словари для хранения:
        - Единиц измерения (measure_key)
        - Номенклатуры продуктов (nomenclature_key) 
        - Групп номенклатуры (nomenclature_group_key)
        - Рецептов (recipe_key)
        - Складов (storage_key)
        - Транзакций (transaction_key)
        """
        self.__repo.initalize()

    def __new__(cls):
        """
        Реализация паттерна Singleton.
        
        Обеспечивает создание только одного экземпляра класса
        во время работы приложения.
        
        Возвращает:
            start_service: Единственный экземпляр класса
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance 
    
    @property
    def repo(self):
        """
        Предоставляет доступ к репозиторию данных.
        
        Возвращает:
            reposity: Репозиторий со всеми данными приложения
        """
        return self.__repo

    def load_data(self) -> bool:
        """
        Загружает данные из файла, если он существует.
        
        Возвращает:
            bool: True если данные успешно загружены, иначе False
        """
        try:
            if os.path.exists(self.__data_file):
                with open(self.__data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                converter = convert_factory()
                loaded_data = converter.convert_back(data["data"])
                
                # Восстанавливаем данные в репозиторий
                self.__repo.data = loaded_data
                print("Данные успешно загружены из файла")
                return True
            return False
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            return False

    def save_data(self) -> bool:
        """
        Сохраняет текущие данные в файл.
        
        Возвращает:
            bool: True если данные успешно сохранены, иначе False
        """
        try:
            self.dump(self.__data_file)
            return True
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")
            return False

    def initialize_application(self, settings_mgr: settings_manager) -> bool:
        """
        Инициализирует приложение в зависимости от настроек первого старта.
        
        Аргументы:
            settings_mgr (settings_manager): Менеджер настроек приложения
            
        Возвращает:
            bool: True если инициализация прошла успешно
            
        Логика:
            - Если first_start = True: создает начальные данные и сохраняет их
            - Если first_start = False: загружает данные из файла
            - Если файл данных не найден: создает новые данные
        """
        if settings_mgr.is_first_start():
            print("Первый запуск приложения. Инициализация данных...")
            # Создаем начальные данные
            self.start()
            # Сохраняем данные
            if self.save_data():
                # Устанавливаем флаг первого запуска в False
                settings_mgr.set_first_start_completed()
                print("Инициализация данных завершена")
                return True
            else:
                print("Ошибка сохранения данных при первом запуске")
                return False
        else:
            print("Загрузка существующих данных...")
            if not self.load_data():
                print("Файл данных не найден. Создание новых данных...")
                self.start()
                self.save_data()
        
        return True

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
        
        Возвращает:
            dict: Словарь со всеми данными приложения
        """
        return self.__repo.data   
    
    def __default_create_recipe_waffles(self):
        """
        Создает рецепт вафель.
        
        Формирует полный рецепт с пошаговой инструкцией и списком ингредиентов.
        Включает все этапы приготовления от подготовки продуктов до выпекания.
        
        Возвращает:
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
        self.__repo.data[reposity.recipe_key()]['Вафли'] = recipe
        return recipe
    
    def __create_omelette_recipe(self):
        """
        Создает рецепт омлета с молоком.
        
        Формирует классический рецепт омлета с подробными шагами приготовления
        и точными пропорциями ингредиентов.
        
        Возвращает:
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
        self.__repo.data[reposity.recipe_key()]['Омлет с молоком'] = recipe
        return recipe
    
    def __create_flatjack_recipe(self):
        """
        Создает рецепт простых лепешек.
        
        Формирует рецепт домашних лепешек с пошаговым описанием процесса
        от замеса теста до выпекания на сковороде.
        
        Возвращает:
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
        self.__repo.data[reposity.recipe_key()]['Простые лепешки'] = recipe
        return recipe

    def __create_storages(self):
        """
        Создает и заполняет справочник складов.
        
        Добавляет в репозиторий базовые склады:
        - Основной склад
        - Резервный склад
        """
        # Создание первого склада - Основной склад
        s1 = storage_model()
        s1.name = "Основной склад"
        s1.address = "ул. Центральная, 1"
        
        # Создание второго склада - Резервный склад
        s2 = storage_model()
        s2.name = "Резервный склад"
        s2.address = "ул. Крестьянская, 47"
        
        # Добавление складов в репозиторий по ключу хранилища
        self.__repo.data[reposity.storage_key()][s1.name] = s1
        self.__repo.data[reposity.storage_key()][s2.name] = s2

    def __create_transactions(self):
        """
        Создает и заполняет справочник транзакций.
        
        Добавляет в репозиторий тестовые транзакции:
        - Поступления товаров на склады
        - Расходы товаров со складов
        """
        # Получение справочников из репозитория
        nomenclature = self.__repo.data[reposity.nomenclature_key()]
        measures = self.__repo.data[reposity.measure_key()]
        storages = self.__repo.data[reposity.storage_key()]
        
        # Транзакция 1: Поступление сахара на основной склад
        t1 = transaction_model()
        t1.name = "Поступление сахара"
        t1.date = "2025-10-25 10:10:00"
        t1.nomenclature = nomenclature.get("Сахар")
        t1.storage = storages.get("Основной склад")
        t1.quantity = 1000.0  # Положительное значение - приход
        t1.measure = measures.get("г")
        
        # Транзакция 2: Расход сахара с основного склада
        t2 = transaction_model()
        t2.name = "Расход сахара"
        t2.date = "2025-10-27 10:10:00"
        t2.nomenclature = nomenclature.get("Сахар")
        t2.storage = storages.get("Основной склад")
        t2.quantity = -200.0  # Отрицательное значение - расход
        t2.measure = measures.get("г")
        
        # Транзакция 3: Поступление муки на резервный склад
        t3 = transaction_model()
        t3.name = "Поступление муки"
        t3.date = "2025-10-26 10:10:00"
        t3.nomenclature = nomenclature.get("Пшеничная мука")
        t3.storage = storages.get("Резервный склад")
        t3.quantity = 5000.0  # Положительное значение - приход
        t3.measure = measures.get("г")
        
        # Транзакция 4: Поступление яиц на основной склад
        t4 = transaction_model()
        t4.name = "Поступление яиц"
        t4.date = "2025-10-24 10:10:00"
        t4.nomenclature = nomenclature.get("Яйца куриные")
        t4.storage = storages.get("Основной склад")
        t4.quantity = 30.0  # Положительное значение - приход
        t4.measure = measures.get("шт")
        
        # Транзакция 5: Расход яиц с основного склада
        t5 = transaction_model()
        t5.name = "Расход яиц"
        t5.date = "2025-10-28 10:10:00"
        t5.nomenclature = nomenclature.get("Яйца куриные")
        t5.storage = storages.get("Основной склад")
        t5.quantity = -5.0  # Отрицательное значение - расход
        t5.measure = measures.get("шт")
        
        # Добавление всех транзакций в репозиторий по уникальному коду
        self.__repo.data[reposity.transaction_key()][t1.unique_code] = t1
        self.__repo.data[reposity.transaction_key()][t2.unique_code] = t2
        self.__repo.data[reposity.transaction_key()][t3.unique_code] = t3
        self.__repo.data[reposity.transaction_key()][t4.unique_code] = t4
        self.__repo.data[reposity.transaction_key()][t5.unique_code] = t5

    def dump(self, filename: str = "data_dump.json"):
        """
        Выгружает в файл JSON-формата все доступные данные из репозитория.
        
        Аргументы:
            filename (str): Имя файла для сохранения данных (по умолчанию "data_dump.json")
            
        Ошибки:
            Exception: В случае ошибки при записи файла
        """
        # Собираем все данные из репозитория
        data_to_dump = {}
        
        # Сохраняем данные в файл
        try:
            # Открываем файл для записи с кодировкой UTF-8
            with open(filename, 'w', encoding='utf-8') as f:
                converter = convert_factory()
                data_to_dump["data"] = converter.convert(self.__repo.data)

                json.dump(data_to_dump, f, ensure_ascii=False, indent=2, default=str)
            print(f"Данные успешно выгружены в файл: {filename}")
        except Exception as e:
            # Обработка возможных ошибок при записи файла
            print(f"Ошибка при выгрузке данных: {e}")

    def create_osv(self, start_date: datetime, end_date: datetime, storage: storage_model):
        """
        Создает оборотно-сальдовую ведомость для указанного склада за период.
        
        Аргументы:
            start_date (datetime): Начальная дата периода
            end_date (datetime): Конечная дата периода
            storage_id (str): Идентификатор склада
        
        Возвращает:
            osv_model: Модель оборотно-сальдовой ведомости
            
        Ошибки:
            Validation error: Если переданный объект склада не является storage_model
        """
        # Получаем транзакции и номенклатуру из репозитория
        transactions = self.__repo.data[reposity.transaction_key()]
        nomenclatures = self.__repo.data[reposity.nomenclature_key()]
        
        # Получаем склад по идентификатору
        storage = self.__repo.data[reposity.storage_key()][storage.name]
        
        # Валидируем, что полученный объект является моделью склада
        validator.validate(storage, storage_model)
        
        # Создаем модель оборотно-сальдовой ведомости
        osv = osv_model.create(start_date, end_date, storage)
        
        # Генерируем строки ведомости на основе транзакций и номенклатуры
        osv.generate_rows(transactions, nomenclatures)
        
        return osv
    
    def start(self):
        """
        Основной метод инициализации всех данных приложения.
        
        Последовательно вызывает методы создания:
        - Единиц измерения
        - Групп номенклатуры
        - Номенклатуры продуктов
        - Рецептов
        - Складов
        - Транзакций
        """
        self.__default_create_measure()
        self.__default_create_nomenclature_group()
        self.__default_create_nomenclature()
        self.__default_create_recipe_waffles()
        self.__create_omelette_recipe()
        self.__create_flatjack_recipe()
        self.__create_storages()
        self.__create_transactions()