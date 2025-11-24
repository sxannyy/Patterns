from datetime import datetime
import connexion
import flask
from flask import abort, jsonify
import logging

from Src.Core.prototype import prototype
from Src.Dto.filter_sorting_dto import filter_sorting_dto
from Src.Logics.factory_entities import factory_entities
from Src.Logics.prototype_report import prototype_report
from Src.Models.balance_model import balance_model
from Src.Models.osv_model import osv_model
from Src.reposity import reposity
from Src.settings_manager import settings_manager
from Src.start_service import start_service
from Src.Convertors.convert_factory import convert_factory

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация Flask приложения
flask_app = connexion.FlaskApp(__name__)
app = flask_app.app

# Инициализация сервисов
data_service = start_service()
data = None
responses_factory = factory_entities()
converter = convert_factory()

@app.route("/", methods=['GET'])
def index():
    """
    Корневой эндпоинт API.
    
    Возвращает:
        JSON с приветственным сообщением и списком доступных эндпоинтов
    """
    logger.info("Обработка корневого запроса")
    return jsonify({
        "message": "Добро пожаловать в кулинарное REST API",
        "endpoints": {
            "api_accessibility": "GET /api/accessibility",
            "recipes_list": "GET /api/recipes", 
            "recipe_by_id": "GET /api/recipes/<recipe_id>",
            "references_list": "GET /api/references",
            "reference_by_name": "GET /api/references/<reference_name>",
            "create_dump": "POST /api/dump",
            "report": "GET /report/<code>/<start>/<end>",
            "filter": "POST /api/<string:domain_name>/filter",
            "OSV": "POST /api/report/osv",
            "set_block_date": "POST /api/settings/block-date",
            "get_block_date": "GET /api/settings/block-date",
            "balances_on_date": "GET /api/balances?date=YYYY-MM-DD%%20HH:MM:SS[&storage=...]"
        }
    })

@app.route("/api/accessibility", methods=['GET'])
def formats():
    """
    Проверить доступность REST API.
    
    Возвращает:
        Строка "SUCCESS" при успешной проверке доступности
    """
    logger.info("Проверка доступности API")
    return "SUCCESS"

@app.route("/response/<string:type>", methods=['GET'])
def get_response(type):
    """
    Получить ответ в указанном формате.
    
    Аргументы:
        type (str): Тип формата ответа (должен быть поддерживаемым форматом)
        
    Возвращает:
        Текст ответа в запрошенном формате
        
    Ошибки:
        404: Если указанный тип формата не поддерживается
    """
    logger.info(f"Запрос ответа в формате: {type}")
    
    # Проверяем поддержку запрошенного формата
    if type not in responses_factory.response_formats:
        logger.warning(f"Неподдерживаемый формат: {type}")
        abort(404, description=f"Формат '{type}' не поддерживается")
    
    # Создаем генератор ответа и генерируем текст
    response = responses_factory.create(type)
    recipe_data = data[reposity.recipe_key()]
    text = response().create(recipe_data)
    
    logger.info(f"Ответ успешно сгенерирован в формате: {type}")
    return text

@app.route("/api/recipes", methods=['GET'])
def get_recipes():
    """
    Получить список всех рецептов в формате JSON.
    
    Возвращает:
        JSON массив со всеми рецептами
        
    Ошибки:
        500: В случае внутренней ошибки сервера при получении рецептов
    """
    logger.info("Запрос списка всех рецептов")
    try:
        # Получаем данные рецептов из репозитория
        recipes_data = data.get(reposity.recipe_key(), {})
        
        # Преобразуем все рецепты в JSON-совместимый формат
        converted_recipes = []
        for recipe_name, recipe in recipes_data.items():
            converted_recipe = converter.convert(recipe)
            converted_recipes.append(converted_recipe)
        
        logger.info(f"Успешно возвращено {len(converted_recipes)} рецептов")
        return jsonify(converted_recipes)
        
    except Exception as e:
        logger.error(f"Ошибка при получении списка рецептов: {str(e)}")
        abort(500, description=f"Ошибка при получении списка рецептов: {str(e)}")

@app.route("/api/recipes/<string:recipe_id>", methods=['GET'])
def get_recipe(recipe_id):
    """
    Получить конкретный рецепт по ID в формате JSON.
    
    Аргументы:
        recipe_id (str): Идентификатор или название рецепта
        
    Возвращает:
        JSON объект с данными рецепта
        
    Ошибки:
        404: Если рецепт с указанным ID не найден
        500: В случае внутренней ошибки сервера
    """
    logger.info(f"Запрос рецепта с идентификатором: {recipe_id}")
    try:
        recipes_data = data.get(reposity.recipe_key(), {})
        
        # Ищем рецепт по уникальному коду или названию
        found_recipe = None
        for recipe_name, recipe in recipes_data.items():
            # Поиск по уникальному коду
            if hasattr(recipe, 'unique_code') and getattr(recipe, 'unique_code', None) == recipe_id:
                found_recipe = recipe
                break
            # Альтернативный поиск по названию
            elif recipe_name == recipe_id:
                found_recipe = recipe
                break
        
        if not found_recipe:
            logger.warning(f"Рецепт с идентификатором '{recipe_id}' не найден")
            abort(404, description=f"Рецепт с идентификатором '{recipe_id}' не найден")
        
        # Преобразуем рецепт в JSON-совместимый формат
        converted_recipe = converter.convert(found_recipe)
        
        logger.info(f"Рецепт с идентификатором '{recipe_id}' успешно найден")
        return jsonify(converted_recipe)
        
    except Exception as e:
        logger.error(f"Ошибка при получении рецепта {recipe_id}: {str(e)}")
        abort(500, description=f"Ошибка при получении рецепта: {str(e)}")

@app.route("/api/references", methods=['GET'])
def get_references():
    """
    Получить список всех справочников в формате JSON.
    
    Возвращает:
        JSON объект со всеми справочниками (кроме рецептов)
        
    Ошибки:
        500: В случае внутренней ошибки сервера при получении справочников
    """
    logger.info("Запрос списка всех справочников")
    try:
        references_data = {}
        
        # Собираем все справочники кроме рецептов
        for key, value in data.items():
            if key != reposity.recipe_key():  # исключаем рецепты
                # Преобразуем каждый элемент справочника
                converted_items = []
                for item_name, item in value.items():
                    converted_item = converter.convert(item)
                    converted_items.append(converted_item)
                
                references_data[key] = converted_items
        
        logger.info(f"Успешно возвращено {len(references_data)} справочников")
        return jsonify(references_data)
        
    except Exception as e:
        logger.error(f"Ошибка при получении справочников: {str(e)}")
        abort(500, description=f"Ошибка при получении справочников: {str(e)}")

@app.route("/api/references/<string:reference_name>", methods=['GET'])
def get_reference(reference_name):
    """
    Получить конкретный справочник по имени в формате JSON.
    
    Аргументы:
        reference_name (str): Название справочника
        
    Возвращает:
        JSON объект с данными справочника
        
    Ошибки:
        404: Если справочник с указанным именем не найден
        500: В случае внутренней ошибки сервера
    """
    logger.info(f"Запрос справочника: {reference_name}")
    try:
        # Проверяем существование справочника
        if reference_name not in data:
            logger.warning(f"Справочник '{reference_name}' не найден")
            abort(404, description=f"Справочник '{reference_name}' не найден")
        
        reference_data = data[reference_name]
        
        # Преобразуем все элементы справочника
        converted_items = []
        for item_name, item in reference_data.items():
            converted_item = converter.convert(item)
            converted_items.append(converted_item)
        
        logger.info(f"Справочник '{reference_name}' содержит {len(converted_items)} элементов")
        return jsonify({
            "reference_name": reference_name,
            "items": converted_items
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении справочника {reference_name}: {str(e)}")
        abort(500, description=f"Ошибка при получении справочника: {str(e)}")

@app.route("/report/<code>/<start>/<end>", methods=['GET'])
def get_report(code, start, end):
    """
    Сгенерировать отчет по складу за указанный период в CSV формате.
    
    Аргументы:
        code (str): Код или название склада
        start (str): Дата начала периода в формате "ГГГГ-ММ-ДД ЧЧ:ММ:СС"
        end (str): Дата окончания периода в формате "ГГГГ-ММ-ДД ЧЧ:ММ:СС"
    """
    logger.info(f"Запрос отчета для склада '{code}' за период {start} - {end}")
    
    # Создаем генератор CSV отчетов
    result_format = factory_entities().create("csv")()
    res = data[reposity.storage_key()]
    storage = None
    
    try:
        # Парсим даты из строкового формата
        start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        finish_date = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.error("Неправильный формат дат в запросе отчета")
        return "Неправильный формат дат! Используйте: ГГГГ-ММ-ДД ЧЧ:ММ:СС"
    
    # Ищем склад по коду или названию
    for key, item in res.items():
        if item.name == code:
            storage = item
            break
            
    if storage is None:
        logger.warning(f"Склад с кодом '{code}' не найден")
        return "Неправильный код склада!"
    
    # Передаем объект storage_model
    osv = data_service.create_osv(start_date, finish_date, storage)
    
    # Генерируем CSV отчет
    result = result_format.create(osv.rows)
    
    logger.info(f"Отчет для склада '{code}' успешно сгенерирован")
    return flask.Response(response=result, status=200, content_type="text/plain;charset=utf-8")

@app.route("/api/dump", methods=['POST'])
def get_dump():
    """
    Сохранить все данные из репозитория в JSON файл.
    
    Тело запроса (JSON, опционально):
    {
        "filename": "имя_файла.json"  # по умолчанию "data_dump.json"
    }
    
    Возвращает:
        JSON ответ с результатом операции
        
    Ошибки:
        500: В случае ошибки при выгрузке данных
    """
    try:
        # Получаем данные из тела запроса
        if flask.request.is_json:
            request_data = flask.request.get_json()
            filename = request_data.get('filename', 'data_dump.json')
        else:
            # Если JSON не предоставлен, используем значение по умолчанию
            filename = 'data_dump.json'
        
        # Проверяем расширение файла
        if not filename.endswith('.json'):
            filename += '.json'
        
        logger.info(f"Запрос на выгрузку данных в файл: {filename}")
        
        # Используем метод dump из start_service для сохранения данных
        data_service.dump(filename)
        
        logger.info(f"Данные успешно выгружены в файл: {filename}")
        
        return jsonify({
            "status": "success",
            "message": f"Данные успешно выгружены в файл: {filename}",
            "filename": filename
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка при выгрузке данных: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Ошибка при выгрузке данных: {str(e)}"
        }), 500
    
@app.route("/api/<string:domain_name>/filter", methods=['POST'])
def filter_domain(domain_name):
    """
    Фильтрация доменных моделей по DTO фильтрации.
    
    Аргументы:
        domain_name: Название доменной модели для фильтрации. Допустимые значения:
            - 'nomenclature' - номенклатура
            - 'nomenclature_groups' - группы номенклатуры
            - 'measure' - единицы измерения
            - 'recipe' - рецепты  
    Возвращает:
        JSON: Отфильтрованный и отсортированный список объектов в формате DTO  
    Ошибки:
        400: Если запрос не содержит JSON или указан неизвестный тип доменной модели
        404: Если указан неизвестный тип доменной модели
        500: При внутренних ошибках обработки
    """
    if not flask.request.is_json:
        abort(400, description="Ожидается JSON в теле запроса")

    request_data = flask.request.get_json()

    # Разбираем DTO фильтрации
    fs_dto = filter_sorting_dto().create(request_data)

    # Маппинг типа в ключ репозитория
    repo_key_map = {
        "nomenclature": reposity.nomenclature_key(),
        "group": reposity.nomenclature_group_key(),
        "measure": reposity.measure_key(),
        "recipe": reposity.recipe_key(),
    }

    if domain_name not in repo_key_map:
        abort(404, description=f"Неизвестный тип доменной модели: {domain_name}")

    repo_key = repo_key_map[domain_name]
    domain_dict = data.get(repo_key, {})

    items = list(domain_dict.values())

    # Оборачиваем в прототип
    proto = prototype_report(items)

    # Последовательно применяем все фильтры
    for filter in fs_dto.filters:
        proto = prototype_report.filter(proto, filter)

    result_items = proto.data

    # Сортировка
    for sort_field in reversed(fs_dto.sorting):
        result_items.sort(
            key=lambda obj: prototype.get_nested_value(obj, sort_field) or ""
        )

    # Конвертируем в JSON через convert_factory
    converter = convert_factory()
    result = converter.convert_list(result_items)

    return jsonify(result)

@app.route("/report/<storage_code>/<start_str>/<end_str>", methods=['POST'])
def get_osv_filtered(storage_code, start_str, end_str):
    """
    Формирование ОСВ (Оборотно-сальдовой ведомости) с учетом DTO фильтрации.
    
    Возвращает:
        JSON: ОСВ в формате CSV с отфильтрованными и отсортированными данными
        
    Ошибки:
        400: Если запрос не содержит JSON или отсутствуют обязательные параметры
        404: Если склад не найден
        500: При внутренних ошибках формирования отчета
    """
    if not flask.request.is_json:
        abort(400, description="Ожидается JSON в теле запроса")

    req = flask.request.get_json()

    if not storage_code or not start_str or not end_str:
        abort(400, description="Нужно указать storage, start и end")

    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        abort(400, description="Неверный формат дат. Ожидается: ГГГГ-ММ-ДД ЧЧ:ММ:СС")

    # Ищем склад по имени (как в GET /report/...)
    storages = data[reposity.storage_key()]
    storage = None
    for item in storages.values():
        if item.name == storage_code or item.unique_code == storage_code:
            storage = item
            break

    if storage is None:
        abort(404, description="Склад не найден")

    # Создаем ОСВ через существующий сервис
    osv_build = data_service.create_osv(start_date, end_date, storage)

    rows = osv_build.rows

    # DTO фильтрации
    fs_dto = filter_sorting_dto().create(req)

    proto = prototype_report(rows)
    for filter in fs_dto.filters:
        proto = prototype_report.filter(proto, filter)

    filtered_rows = proto.data

    # Формируем модель ОСВ с отфильтрованными строками
    osv = osv_model.create(start_date, end_date, storage)
    osv.rows = filtered_rows

    result_format = factory_entities().create("csv")()
    osv_dto_dict = result_format.create(osv.rows)

    return  flask.Response(
        response=osv_dto_dict,
        status=200,
        content_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment;filename=report.csv"}
    )

@app.route("/api/settings/block-date", methods=['POST'])
def set_block_date():
    """
    Установить или изменить дату блокировки (block_date) в настройках.

    Тело запроса (JSON):
    {
        "block_date": "ГГГГ-ММ-ДД ЧЧ:ММ:СС" | null
    }

    Логика:
        - Если block_date = null или отсутствует — дата блокировки сбрасывается (None),
          кэш очищается, данные и настройки сохраняются.
        - Если указана строка — парсим в datetime, устанавливаем в start_service.block_date
          (пересчитывается кэш), сохраняем данные (dump) и обновляем settings.json.
    """
    if not flask.request.is_json:
        abort(400, description="Ожидается JSON в теле запроса")

    req = flask.request.get_json()
    block_date_str = req.get("block_date", None)

    # Сброс даты блокировки
    if block_date_str in (None, "", "null"):
        logger.info("Сброс даты блокировки (block_date = None)")

        # Обновляем сервис
        data_service.block_date = None

        # Обновляем настройки
        settings_mgr.settings.block_date = None
        settings_mgr.save_settings()

        # Сохраняем текущие данные (без кэша)
        data_service.save_data()

        return jsonify({
            "status": "success",
            "block_date": None
        }), 200

    # Установка новой даты блокировки
    try:
        new_block_date = datetime.strptime(block_date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.error(f"Неверный формат даты блокировки: {block_date_str}")
        abort(400, description="Неверный формат даты. Ожидается: ГГГГ-ММ-ДД ЧЧ:ММ:СС")

    logger.info(f"Установка новой даты блокировки: {block_date_str}")

    # 1. Обновляем сервис (пересчёт кэша остатков)
    data_service.block_date = new_block_date

    # 2. Обновляем настройки
    settings_mgr.settings.block_date = new_block_date
    settings_mgr.save_settings()

    # 3. Автоматически сохраняем все данные (включая кэш) в data_dump / app_data.json
    data_service.save_data()

    return jsonify({
        "status": "success",
        "block_date": block_date_str
    }), 200

@app.route("/api/settings/block-date", methods=['GET'])
def get_block_date():
    """
    Получить текущую дату блокировки (block_date) из сервиса.

    Возвращает:
        { "block_date": "ГГГГ-ММ-ДД ЧЧ:ММ:СС" | null }
    """
    block_date = getattr(data_service, "block_date", None)

    if isinstance(block_date, datetime):
        block_date_str = block_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        block_date_str = None

    logger.info(f"Текущая дата блокировки: {block_date_str}")

    return jsonify({
        "block_date": block_date_str
    }), 200

@app.route("/api/balances/<string:date_str>", methods=['GET'])
@app.route("/api/balances/<string:date_str>/<string:storage_code>", methods=['GET'])
def get_balances_on_date(date_str, storage_code=None):
    """
    Получить остатки на указанную дату.

    Параметры:
        /api/balances/<date_str>
        /api/balances/<date_str>/<storage_code>

    Где:
        date_str: "ГГГГ-ММ-ДД ЧЧ:ММ:СС"
        storage_code: имя или unique_code склада

    Примеры:
        GET /api/balances/2025-10-25 00:00:00
        GET /api/balances/2025-10-25 00:00:00/Основной склад
    """
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        abort(400, description="Неверный формат даты. Ожидается: ГГГГ-ММ-ДД ЧЧ:ММ:СС")

    logger.info(f"Запрос остатков на дату {date_str} (storage={storage_code})")

    # Данные из глобального репозитория
    transactions_data = data.get(reposity.transaction_key(), {})
    storages_data = data.get(reposity.storage_key(), {})
    nomenclatures_data = data.get(reposity.nomenclature_key(), {})

    if not transactions_data:
        abort(500, description="В репозитории отсутствуют транзакции")

    # Фильтрация складов по storage_code
    allowed_storages = list(storages_data.values())
    if storage_code:
        allowed_storages = [
            s for s in storages_data.values()
            if s.name == storage_code or getattr(s, "unique_code", None) == storage_code
        ]
        if not allowed_storages:
            abort(404, description="Склад не найден по параметру storage_code")
    allowed_storage_ids = {s.unique_code for s in allowed_storages}

    # Агрегируем остатки по ключу (storage_id, nomenclature_id)
    balances_by_key: dict[tuple[str, str], balance_model] = {}

    for tr in transactions_data.values():
        # Берём только транзакции, которые произошли не позже целевой даты
        if tr.date > target_date:
            continue

        storage = tr.storage
        if storage.unique_code not in allowed_storage_ids:
            continue

        nomenclature = tr.nomenclature

        # Базовая единица измерения для номенклатуры
        base_measure = nomenclature.measure.base_measure or nomenclature.measure

        quantity = tr.quantity

        # Конвертация количества в базовую единицу измерения
        if tr.measure.base_measure and tr.measure.base_measure == base_measure:
            quantity *= tr.measure.conversion_factor

        key = (storage.unique_code, nomenclature.unique_code)

        if key not in balances_by_key:
            balance_item = balance_model.create(
                nomenclature=nomenclature,
                measure=base_measure,
                end_balance=0.0,
                block_date=target_date
            )
            balance_item.storage = storage
            balances_by_key[key] = balance_item

        balances_by_key[key].end_balance = balances_by_key[key].end_balance + quantity

    balance_list = list(balances_by_key.values())

    try:
        result = converter.convert_list(balance_list)
    except Exception:
        result = [
            {
                "storage_id": b.storage.unique_code,
                "storage_name": b.storage.name,
                "nomenclature_id": b.nomenclature.unique_code,
                "nomenclature_name": b.nomenclature.name,
                "measure_id": b.measure.unique_code,
                "measure_name": b.measure.name,
                "end_balance": b.end_balance,
                "block_date": b.block_date.strftime("%Y-%m-%d %H:%M:%S")
                    if isinstance(b.block_date, datetime) else None
            }
            for b in balance_list
        ]

    logger.info(f"Найдено {len(balance_list)} остатков на дату {date_str}")

    return jsonify(result), 200

@app.errorhandler(404)
def page_not_found(error):
    """
    Обработчик ошибки 404 - Ресурс не найден.
    
    Аргументы:
        error: Объект ошибки
        
    Возвращает:
        JSON ответ с описанием ошибки
    """
    logger.error(f"Ошибка 404: {error}")
    return jsonify({
        "error": "Запрашиваемый ресурс не найден.", 
        "status": 404
    }), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Обработчик ошибки 500 - Внутренняя ошибка сервера.
    
    Аргументы:
        error: Объект ошибки
        
    Возвращает:
        JSON ответ с описанием ошибки
    """
    logger.error(f"Ошибка 500: {error}")
    return jsonify({
        "error": f"Внутренняя ошибка сервера: {str(error)}", 
        "status": 500
    }), 500

if __name__ == '__main__':
    """
    Точка входа приложения.
    Запускает сервис данных и Flask сервер.
    """
    # Запускаем сервис данных и получаем данные репозитория
    data_service.start()
    data = data_service.repo.data
    settings_mgr = settings_manager("settings.json")
    settings_mgr.load_settings()
    data_service.block_date = settings_mgr.settings.block_date
    
    logger.info("Сервис запущен на 0.0.0.0:8080")
    
    # Запускаем Flask приложение
    app.run(host="0.0.0.0", port=8080)