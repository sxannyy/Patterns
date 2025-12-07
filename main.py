from datetime import datetime
import connexion
import flask
from flask import abort, jsonify

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
from Src.Logics.reference_service import reference_service
from Src.Core.validator import argument_exception

from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Dto.log_event_dto import log_event_dto

try:
    from Src.Core.logger import logger as observe_logger
except Exception:
    observe_logger = None

def emit(event: str, message: str, data: dict = None, exc: Exception = None):
    """ 
    Внутренний помощник для отправки событий логирования.

    Формирует log_event_dto и публикует событие через observe_service.

    Аргументы:
        event (str): Тип события логирования (event_type.*_log()).
        message (str): Текст сообщения.
        data (dict, optional): Дополнительные данные контекста.
        exc (Exception, optional): Исключение для фиксации в логе.

    Примечания:
        Исключение сохраняется в DTO в виде строки, 
        чтобы избежать проблем сериализации.
    """
    dto = log_event_dto()
    dto.message = message
    dto.data = data or {}
    if exc is not None:
        dto.exception = str(exc)
    observe_service.create_event(event, dto)

def log_debug(message: str, data: dict = None):
    """ 
    Логирование отладочного сообщения.

    Аргументы:
        message (str): Текст сообщения.
        data (dict, optional): Дополнительные данные.
    """
    emit(event_type.debug_log(), message, data=data)

def log_info(message: str, data: dict = None):
    """ 
    Логирование информационного сообщения.

    Аргументы:
        message (str): Текст сообщения.
        data (dict, optional): Дополнительные данные.
    """
    emit(event_type.info_log(), message, data=data)

def log_warning(message: str, data: dict = None):
    """ 
    Логирование предупреждения.

    Аргументы:
        message (str): Текст сообщения.
        data (dict, optional): Дополнительные данные.
    """
    emit(event_type.warning_log(), message, data=data)

def log_error(message: str, exc: Exception = None, data: dict = None):
    """ 
    Логирование ошибки.

    Аргументы:
        message (str): Текст сообщения.
        exc (Exception, optional): Исключение.
        data (dict, optional): Дополнительные данные.
    """
    emit(event_type.error_log(), message, data=data, exc=exc)

""" 
Инициализация Connexion/Flask приложения
"""
flask_app = connexion.FlaskApp(__name__)
app = flask_app.app

""" 
Инициализация сервисов доменной логики и инфраструктуры.

data_service:
    Основной сервис данных (старт/загрузка/доступ к репозиториям).
data:
    Ссылка на словарь данных репозитория.
responses_factory:
    Фабрика форматов ответа (csv/json и т.п.).
converter:
    Фабрика конвертеров доменных моделей в DTO/словари.
ref_service:
    Сервис справочников (инициализируется после загрузки данных).
settings_mgr:
    Менеджер настроек (инициализируется при запуске приложения).
"""

data_service = start_service()
data = None
responses_factory = factory_entities()
converter = convert_factory()
ref_service = None
settings_mgr = None

# Endpoints: базовые и информационные

@app.route("/", methods=['GET'])
def index():
    """ 
    Корневой эндпоинт API.
    Возвращает краткое описание сервиса и список основных маршрутов.
    """
    log_info("Обработка корневого запроса")
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
            "balances_on_date": "GET /api/balances?date=YYYY-MM-DD%%20HH:MM:SS[&storage=...]",
            "reference_operations": {
                "get_reference_item": "GET /api/<reference_type>?unique_code=...",
                "add_reference_item": "PUT /api/<reference_type>",
                "update_reference_item": "PATCH /api/<reference_type>",
                "delete_reference_item": "DELETE /api/<reference_type>?unique_code=..."
            }
        }
    })

@app.route("/api/accessibility", methods=['GET'])
def formats():
    """ 
    Тестовый эндпоинт доступности API.

    Возвращает:
        str: Статус доступности сервиса.
    """
    log_info("Проверка доступности API")
    return "SUCCESS"

# Endpoints: форматы ответа и рецепты

@app.route("/response/<string:type>", methods=['GET'])
def get_response(type):
    """ 
    Возвращает данные рецептов в указанном формате ответа.
    Аргументы:
        type (str): Название формата ответа.
    Исключения:
        404: Если формат не поддерживается.
    Возвращает:
        str: Сформированный текст ответа в выбранном формате.
    """
    log_info("Запрос ответа в формате", {"type": type})

    if type not in responses_factory.response_formats:
        log_warning("Неподдерживаемый формат ответа", {"type": type})
        abort(404, description=f"Формат '{type}' не поддерживается")

    response = responses_factory.create(type)
    recipe_data = data[reposity.recipe_key()]
    text = response().create(recipe_data)

    log_info("Ответ успешно сгенерирован", {"type": type})
    return text

@app.route("/api/recipes", methods=['GET'])
def get_recipes():
    """ 
    Возвращает список всех рецептов.

    Логика:
        - извлекает рецепты из репозитория
        - конвертирует в DTO/словарный формат

    Возвращает:
        flask.Response: JSON список рецептов.

    Исключения:
        500: При внутренней ошибке чтения/конвертации.
    """
    log_info("Запрос списка всех рецептов")
    try:
        recipes_data = data.get(reposity.recipe_key(), {})

        converted_recipes = []
        for recipe_name, recipe in recipes_data.items():
            converted_recipe = converter.convert(recipe)
            converted_recipes.append(converted_recipe)

        log_info("Успешно возвращено рецептов", {"count": len(converted_recipes)})
        return jsonify(converted_recipes)

    except Exception as e:
        log_error("Ошибка при получении списка рецептов", e)
        abort(500, description=f"Ошибка при получении списка рецептов: {str(e)}")

@app.route("/api/recipes/<string:recipe_id>", methods=['GET'])
def get_recipe(recipe_id):
    """ 
    Возвращает рецепт по идентификатору.

    Поиск выполняется:
        - по unique_code объекта рецепта
        - либо по ключу словаря рецептов

    Аргументы:
        recipe_id (str): Идентификатор рецепта.

    Возвращает:
        flask.Response: JSON объект рецепта.

    Исключения:
        404: Если рецепт не найден.
        500: При внутренней ошибке.
    """
    log_info("Запрос рецепта", {"recipe_id": recipe_id})
    try:
        recipes_data = data.get(reposity.recipe_key(), {})

        found_recipe = None
        for recipe_name, recipe in recipes_data.items():
            if hasattr(recipe, 'unique_code') and getattr(recipe, 'unique_code', None) == recipe_id:
                found_recipe = recipe
                break
            elif recipe_name == recipe_id:
                found_recipe = recipe
                break

        if not found_recipe:
            log_warning("Рецепт не найден", {"recipe_id": recipe_id})
            abort(404, description=f"Рецепт с идентификатором '{recipe_id}' не найден")

        converted_recipe = converter.convert(found_recipe)

        log_info("Рецепт успешно найден", {"recipe_id": recipe_id})
        return jsonify(converted_recipe)

    except Exception as e:
        log_error("Ошибка при получении рецепта", e, {"recipe_id": recipe_id})
        abort(500, description=f"Ошибка при получении рецепта: {str(e)}")

# Endpoints: справочники

@app.route("/api/references", methods=['GET'])
def get_references():
    """ 
    Возвращает набор всех справочников.

    Логика:
        - перебирает ключи репозитория
        - исключает рецепты
        - конвертирует элементы каждого справочника

    Возвращает:
        flask.Response: JSON словарь {reference_name: [items]}.

    Исключения:
        500: При внутренней ошибке.
    """
    log_info("Запрос списка всех справочников")
    try:
        references_data = {}

        for key, value in data.items():
            if key != reposity.recipe_key():
                converted_items = []
                for item_name, item in value.items():
                    converted_item = converter.convert(item)
                    converted_items.append(converted_item)

                references_data[key] = converted_items

        log_info("Успешно возвращено справочников", {"count": len(references_data)})
        return jsonify(references_data)

    except Exception as e:
        log_error("Ошибка при получении справочников", e)
        abort(500, description=f"Ошибка при получении справочников: {str(e)}")

@app.route("/api/references/<string:reference_name>", methods=['GET'])
def get_reference(reference_name):
    """ 
    Возвращает справочник по имени.

    Аргументы:
        reference_name (str): Имя справочника.

    Возвращает:
        flask.Response: JSON объект {reference_name, items}.

    Исключения:
        404: Если справочник не найден.
        500: При внутренней ошибке.
    """
    log_info("Запрос справочника", {"reference_name": reference_name})
    try:
        if reference_name not in data:
            log_warning("Справочник не найден", {"reference_name": reference_name})
            abort(404, description=f"Справочник '{reference_name}' не найден")

        reference_data = data[reference_name]

        converted_items = []
        for item_name, item in reference_data.items():
            converted_item = converter.convert(item)
            converted_items.append(converted_item)

        log_info("Справочник содержит элементов", {
            "reference_name": reference_name,
            "count": len(converted_items)
        })

        return jsonify({
            "reference_name": reference_name,
            "items": converted_items
        })

    except Exception as e:
        log_error("Ошибка при получении справочника", e, {"reference_name": reference_name})
        abort(500, description=f"Ошибка при получении справочника: {str(e)}")

# Endpoints: отчеты

@app.route("/report/<code>/<start>/<end>", methods=['GET'])
def get_report(code, start, end):
    """ 
    Формирует отчет по складу за период.

    Аргументы:
        code (str): Код/имя склада.
        start (str): Дата начала периода в формате "%Y-%m-%d %H:%M:%S".
        end (str): Дата окончания периода в формате "%Y-%m-%d %H:%M:%S".

    Возвращает:
        flask.Response | str: CSV-данные или текст ошибки формата входных дат/кода склада.
    """
    log_info("Запрос отчета", {"storage_code": code, "start": start, "end": end})

    result_format = factory_entities().create("csv")()
    res = data[reposity.storage_key()]
    storage = None

    try:
        start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        finish_date = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        log_error("Неправильный формат дат в запросе отчета")
        return "Неправильный формат дат! Используйте: ГГГГ-ММ-ДД ЧЧ:ММ:СС"

    for key, item in res.items():
        if item.name == code:
            storage = item
            break

    if storage is None:
        log_warning("Склад не найден для отчета", {"storage_code": code})
        return "Неправильный код склада!"

    osv = data_service.create_osv(start_date, finish_date, storage)
    result = result_format.create(osv.rows)

    log_info("Отчет успешно сгенерирован", {"storage_code": code})
    return flask.Response(response=result, status=200, content_type="text/plain;charset=utf-8")

@app.route("/api/dump", methods=['POST'])
def get_dump():
    """ 
    Создает JSON-дамп данных репозитория.

    Тело запроса (опционально):
        { "filename": "имя_файла.json" }

    Возвращает:
        flask.Response: JSON со статусом операции.

    Исключения:
        500: При ошибке выгрузки.
    """
    try:
        if flask.request.is_json:
            request_data = flask.request.get_json()
            filename = request_data.get('filename', 'data_dump.json')
        else:
            filename = 'data_dump.json'

        if not filename.endswith('.json'):
            filename += '.json'

        log_info("Запрос на выгрузку данных", {"filename": filename})

        data_service.dump(filename)

        log_info("Данные успешно выгружены", {"filename": filename})

        return jsonify({
            "status": "success",
            "message": f"Данные успешно выгружены в файл: {filename}",
            "filename": filename
        }), 200

    except Exception as e:
        log_error("Ошибка при выгрузке данных", e)
        return jsonify({
            "status": "error",
            "message": f"Ошибка при выгрузке данных: {str(e)}"
        }), 500

# Endpoints: фильтрация доменных моделей

@app.route("/api/<string:domain_name>/filter", methods=['POST'])
def filter_domain(domain_name):
    """ 
    Фильтрация и сортировка доменных сущностей.

    Ожидает JSON тело запроса, совместимое с filter_sorting_dto.

    Аргументы:
        domain_name (str): Имя доменной области:
            - nomenclature
            - group
            - measure
            - recipe

    Возвращает:
        flask.Response: JSON список отфильтрованных объектов.

    Исключения:
        400: Если тело запроса не JSON.
        404: Если domain_name не поддерживается.
    """
    if not flask.request.is_json:
        abort(400, description="Ожидается JSON в теле запроса")

    request_data = flask.request.get_json()
    fs_dto = filter_sorting_dto().create(request_data)

    repo_key_map = {
        "nomenclature": reposity.nomenclature_key(),
        "group": reposity.nomenclature_group_key(),
        "measure": reposity.measure_key(),
        "recipe": reposity.recipe_key(),
    }

    if domain_name not in repo_key_map:
        log_warning("Неизвестный тип доменной модели для фильтрации", {"domain_name": domain_name})
        abort(404, description=f"Неизвестный тип доменной модели: {domain_name}")

    repo_key = repo_key_map[domain_name]
    domain_dict = data.get(repo_key, {})

    items = list(domain_dict.values())
    proto = prototype_report(items)

    for filter in fs_dto.filters:
        proto = prototype_report.filter(proto, filter)

    result_items = proto.data

    for sort_field in reversed(fs_dto.sorting):
        result_items.sort(
            key=lambda obj: prototype.get_nested_value(obj, sort_field) or ""
        )

    converter = convert_factory()
    result = converter.convert_list(result_items)

    log_info("Фильтрация выполнена", {"domain_name": domain_name, "count": len(result_items)})

    return jsonify(result)

@app.route("/report/<storage_code>/<start_str>/<end_str>", methods=['POST'])
def get_osv_filtered(storage_code, start_str, end_str):
    """ 
    Формирует ОСВ с фильтрацией строк по правилам из filter_sorting_dto.

    Аргументы:
        storage_code (str): Код/имя склада.
        start_str (str): Дата начала периода.
        end_str (str): Дата окончания периода.

    Возвращает:
        flask.Response: CSV файл отчета.

    Исключения:
        400: Некорректные параметры/формат дат/отсутствие JSON.
        404: Если склад не найден.
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

    storages = data[reposity.storage_key()]
    storage = None
    for item in storages.values():
        if item.name == storage_code or item.unique_code == storage_code:
            storage = item
            break

    if storage is None:
        log_warning("Склад не найден для ОСВ", {"storage_code": storage_code})
        abort(404, description="Склад не найден")

    osv_build = data_service.create_osv(start_date, end_date, storage)
    rows = osv_build.rows

    fs_dto = filter_sorting_dto().create(req)

    proto = prototype_report(rows)
    for filter in fs_dto.filters:
        proto = prototype_report.filter(proto, filter)

    filtered_rows = proto.data

    osv = osv_model.create(start_date, end_date, storage)
    osv.rows = filtered_rows

    result_format = factory_entities().create("csv")()
    osv_dto_dict = result_format.create(osv.rows)

    log_info("ОСВ сформирована с фильтрацией", {"storage_code": storage_code, "rows": len(filtered_rows)})

    return flask.Response(
        response=osv_dto_dict,
        status=200,
        content_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment;filename=report.csv"}
    )

# Endpoints: настройки (дата блокировки)

@app.route("/api/settings/block-date", methods=['POST'])
def set_block_date():
    """ 
    Устанавливает или сбрасывает дату блокировки.

    Ожидаемый JSON:
        { "block_date": "YYYY-MM-DD HH:MM:SS" }
    Для сброса:
        { "block_date": null } или пустое значение.

    Возвращает:
        flask.Response: JSON со статусом и установленной датой.

    Исключения:
        400: Неверный формат или отсутствие JSON.
    """
    if not flask.request.is_json:
        abort(400, description="Ожидается JSON в теле запроса")

    req = flask.request.get_json()
    block_date_str = req.get("block_date", None)

    if block_date_str in (None, "", "null"):
        log_info("Сброс даты блокировки (block_date = None)")

        data_service.block_date = None

        settings_mgr.settings.block_date = None
        settings_mgr.save_settings()

        data_service.save_data()

        return jsonify({
            "status": "success",
            "block_date": None
        }), 200

    try:
        new_block_date = datetime.strptime(block_date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        log_error("Неверный формат даты блокировки", data={"block_date": block_date_str})
        abort(400, description="Неверный формат даты. Ожидается: ГГГГ-ММ-ДД ЧЧ:ММ:СС")

    log_info("Установка новой даты блокировки", {"block_date": block_date_str})

    data_service.block_date = new_block_date

    settings_mgr.settings.block_date = new_block_date
    settings_mgr.save_settings()

    data_service.save_data()

    return jsonify({
        "status": "success",
        "block_date": block_date_str
    }), 200

@app.route("/api/settings/block-date", methods=['GET'])
def get_block_date():
    """ 
    Возвращает текущую дату блокировки.

    Возвращает:
        flask.Response: JSON вида { "block_date": "YYYY-MM-DD HH:MM:SS" | None }.
    """
    block_date = getattr(data_service, "block_date", None)

    if isinstance(block_date, datetime):
        block_date_str = block_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        block_date_str = None

    log_info("Запрос текущей даты блокировки", {"block_date": block_date_str})

    return jsonify({
        "block_date": block_date_str
    }), 200

# Endpoints: остатки

@app.route("/api/balances/<string:date_str>", methods=['GET'])
@app.route("/api/balances/<string:date_str>/<string:storage_code>", methods=['GET'])
def get_balances_on_date(date_str, storage_code=None):
    """ 
    Возвращает остатки номенклатуры на указанную дату.

    Аргументы:
        date_str (str): Дата в формате "%Y-%m-%d %H:%M:%S".
        storage_code (str, optional): Код/имя склада для ограничения выборки.

    Логика:
        - фильтрует транзакции по дате
        - учитывает базовые единицы измерения и коэффициенты пересчета
        - агрегирует остатки по складу и номенклатуре

    Возвращает:
        flask.Response: JSON список остатков.

    Исключения:
        400: Неверный формат даты.
        404: Если склад по storage_code не найден.
        500: Если отсутствуют транзакции или внутренняя ошибка.
    """
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        abort(400, description="Неверный формат даты. Ожидается: ГГГГ-ММ-ДД ЧЧ:ММ:СС")

    log_info("Запрос остатков на дату", {"date": date_str, "storage": storage_code})

    transactions_data = data.get(reposity.transaction_key(), {})
    storages_data = data.get(reposity.storage_key(), {})
    nomenclatures_data = data.get(reposity.nomenclature_key(), {})

    if not transactions_data:
        log_error("В репозитории отсутствуют транзакции")
        abort(500, description="В репозитории отсутствуют транзакции")

    allowed_storages = list(storages_data.values())
    if storage_code:
        allowed_storages = [
            s for s in storages_data.values()
            if s.name == storage_code or getattr(s, "unique_code", None) == storage_code
        ]
        if not allowed_storages:
            log_warning("Склад не найден по storage_code", {"storage_code": storage_code})
            abort(404, description="Склад не найден по параметру storage_code")

    allowed_storage_ids = {s.unique_code for s in allowed_storages}

    balances_by_key: dict[tuple[str, str], balance_model] = {}

    for tr in transactions_data.values():
        if tr.date > target_date:
            continue

        storage = tr.storage
        if storage.unique_code not in allowed_storage_ids:
            continue

        nomenclature = tr.nomenclature
        base_measure = nomenclature.measure.base_measure or nomenclature.measure

        quantity = tr.quantity

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

    log_info("Найдено остатков на дату", {"count": len(balance_list), "date": date_str})

    return jsonify(result), 200

# Endpoints: операции со справочниками (CRUD)

@app.route("/api/<string:reference_type>", methods=['GET'])
def get_reference_item(reference_type):
    """ 
    Возвращает один элемент справочника по unique_code.

    Параметры строки запроса:
        unique_code (str): Уникальный код элемента.

    Аргументы:
        reference_type (str): Тип справочника.

    Возвращает:
        flask.Response: JSON объект элемента.

    Исключения:
        400: Некорректные аргументы.
        404: Элемент не найден.
        500: Внутренняя ошибка.
    """
    try:
        unique_code = flask.request.args.get('unique_code')

        if not unique_code:
            abort(400, description="Параметр unique_code обязателен")

        log_info("Запрос элемента справочника", {
            "reference_type": reference_type,
            "unique_code": unique_code
        })

        item = ref_service.get_one(reference_type, unique_code)

        if not item:
            log_warning("Элемент справочника не найден", {
                "reference_type": reference_type,
                "unique_code": unique_code
            })
            abort(404, description=f"Элемент с кодом '{unique_code}' не найден в справочнике '{reference_type}'")

        converted_item = converter.convert(item)

        log_info("Элемент справочника найден", {
            "reference_type": reference_type,
            "unique_code": unique_code
        })

        return jsonify(converted_item), 200

    except argument_exception as e:
        log_error("Ошибка при получении элемента справочника", e)
        abort(400, description=str(e))
    except Exception as e:
        log_error("Ошибка при получении элемента справочника", e)
        abort(500, description=f"Ошибка при получении элемента справочника: {str(e)}")

@app.route("/api/<string:reference_type>", methods=['PUT'])
def add_reference_item(reference_type):
    """ 
    Добавляет новый элемент в указанный справочник.

    Ожидает JSON тело, совместимое с моделью справочника.

    Аргументы:
        reference_type (str): Тип справочника.

    Возвращает:
        flask.Response: JSON объект созданного элемента, статус 201.

    Исключения:
        400: Некорректные аргументы/тело запроса.
        500: Внутренняя ошибка.
    """
    try:
        if not flask.request.is_json:
            abort(400, description="Ожидается JSON в теле запроса")

        request_data = flask.request.get_json()

        log_info("Запрос на добавление элемента справочника", {"reference_type": reference_type})

        item = converter.convert({reference_type: [request_data]})[reference_type][0]

        added_item = ref_service.add(reference_type, item)

        converted_item = converter.convert(added_item)

        log_info("Элемент успешно добавлен", {"reference_type": reference_type})

        return jsonify(converted_item), 201

    except argument_exception as e:
        log_error("Ошибка при добавлении элемента справочника", e)
        abort(400, description=str(e))
    except Exception as e:
        log_error("Ошибка при добавлении элемента справочника", e)
        abort(500, description=f"Ошибка при добавлении элемента: {str(e)}")

@app.route("/api/<string:reference_type>", methods=['PATCH'])
def update_reference_item(reference_type):
    """ 
    Обновляет существующий элемент справочника.

    Ожидаемый JSON:
        {
            "unique_code": "...",
            "changes": { ... }
        }

    Аргументы:
        reference_type (str): Тип справочника.

    Возвращает:
        flask.Response: JSON обновленного элемента.

    Исключения:
        400: Некорректные аргументы/тело запроса.
        500: Внутренняя ошибка.
    """
    try:
        if not flask.request.is_json:
            abort(400, description="Ожидается JSON в теле запроса")

        request_data = flask.request.get_json()
        unique_code = request_data.get('unique_code')
        changes = request_data.get('changes', {})

        if not unique_code:
            abort(400, description="Параметр unique_code обязателен")

        if not changes:
            abort(400, description="Параметр changes обязателен")

        log_info("Запрос на обновление элемента справочника", {
            "reference_type": reference_type,
            "unique_code": unique_code
        })

        updated_item = ref_service.update(reference_type, unique_code, changes)

        converted_item = converter.convert(updated_item)

        log_info("Элемент успешно обновлен", {
            "reference_type": reference_type,
            "unique_code": unique_code
        })

        return jsonify(converted_item), 200

    except argument_exception as e:
        log_error("Ошибка при обновлении элемента справочника", e)
        abort(400, description=str(e))
    except Exception as e:
        log_error("Ошибка при обновлении элемента справочника", e)
        abort(500, description=f"Ошибка при обновлении элемента: {str(e)}")

@app.route("/api/<string:reference_type>", methods=['DELETE'])
def delete_reference_item(reference_type):
    """ 
    Удаляет элемент справочника по unique_code.

    Параметры строки запроса:
        unique_code (str): Уникальный код элемента.

    Аргументы:
        reference_type (str): Тип справочника.

    Возвращает:
        flask.Response: JSON статус операции.

    Исключения:
        400: Некорректные аргументы.
        500: Внутренняя ошибка.
    """
    try:
        unique_code = flask.request.args.get('unique_code')

        if not unique_code:
            abort(400, description="Параметр unique_code обязателен")

        log_info("Запрос на удаление элемента справочника", {
            "reference_type": reference_type,
            "unique_code": unique_code
        })

        result = ref_service.delete(reference_type, unique_code)

        log_info("Элемент успешно удален", {
            "reference_type": reference_type,
            "unique_code": unique_code
        })

        return jsonify({
            "status": "success",
            "message": f"Элемент с кодом '{unique_code}' успешно удален из справочника '{reference_type}'"
        }), 200

    except argument_exception as e:
        log_error("Ошибка при удалении элемента справочника", e)
        return jsonify({
            "status": "error",
            "message": f"Ошибка при удалении элемента: {str(e)}"
        }), 400
    except Exception as e:
        log_error("Ошибка при удалении элемента справочника", e)
        return jsonify({
            "status": "error",
            "message": f"Ошибка при удалении элемента: {str(e)}"
        }), 500

# Глобальные обработчики ошибок

@app.errorhandler(404)
def page_not_found(error):
    """ 
    Обработчик ошибки 404.

    Аргументы:
        error: объект ошибки Flask.

    Возвращает:
        flask.Response: JSON описание ошибки.
    """
    log_error("Ошибка 404", data={"error": str(error)})
    return jsonify({
        "error": "Запрашиваемый ресурс не найден.",
        "status": 404
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    """ 
    Обработчик ошибки 500.

    Аргументы:
        error: объект ошибки Flask.

    Возвращает:
        flask.Response: JSON описание внутренней ошибки сервера.
    """
    log_error("Ошибка 500", data={"error": str(error)})
    return jsonify({
        "error": f"Внутренняя ошибка сервера: {str(error)}",
        "status": 500
    }), 500

# Точка входа приложения

if __name__ == '__main__':

    # Запускаем сервис данных и получаем данные репозитория
    data_service.start()
    data = data_service.repo.data

    # Загружаем настройки
    settings_mgr = settings_manager("settings.json")
    settings_mgr.load_settings()
    data_service.block_date = settings_mgr.settings.block_date

    # Подключаем observer-логгер
    if observe_logger is not None:
        try:
            observe_logger(settings_mgr.settings)
            log_info("Observer logger initialized from settings.")
        except Exception as e:
            # ЭТОТ ПРИНТ ДЛЯ ПОКАЗА ОШИБКИ ИНИЦИАЛИЗАЦИИ ЛОГГЕРА!
            # нужно, чтобы показало, что логгер не работает, но работа сервиса не останавливается
            print(f"Logger init error: {e}")

    # Инициализируем сервис справочников
    ref_service = reference_service(data_service.repo, data_service, settings_mgr)

    log_info("Сервис запущен", {"host": "0.0.0.0", "port": 8080})

    # Запускаем Flask приложение
    app.run(host="0.0.0.0", port=8080)