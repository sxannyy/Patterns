from datetime import datetime
import connexion
import flask
from flask import abort, jsonify
import logging

from Src.Logics.factory_entities import factory_entities
from Src.reposity import reposity
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
            "report": "GET /report/<code>/<start>/<end>"
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
    recipe_data = data[reposity.recipe_key()]['Омлет с молоком']
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
        
    Возвращает:
        CSV отчет в виде текста или сообщение об ошибке
        
    Ошибки:
        Сообщение об ошибке при неверном формате дат или коде склада
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
    
    # Создаем оборотно-сальдовую ведомость
    osv = data_service.create_osv(start_date, finish_date, storage.unique_code)
    
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
    
    logger.info("Сервис запущен на 0.0.0.0:8080")
    
    # Запускаем Flask приложение
    app.run(host="0.0.0.0", port=8080)