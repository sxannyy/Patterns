import connexion
from flask import abort, jsonify
import logging

from Src.Logics.factory_entities import factory_entities
from Src.reposity import reposity
from Src.start_service import start_service
from Src.Convertors.convert_factory import convert_factory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

flask_app = connexion.FlaskApp(__name__)
app = flask_app.app
data_service = start_service()
data = None
responses_factory = factory_entities()
converter = convert_factory()

"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    logger.info("Проверка доступности API")
    return "SUCCESS"

@app.route("/response/<string:type>", methods=['GET'])
def get_response(type):
    logger.info(f"Запрос ответа в формате: {type}")
    if type not in responses_factory.response_formats:
        logger.warning(f"Неверный формат: {type}")
        abort(404)
    response = responses_factory.create(type)
    recipe_data = data[reposity.recipe_key()]['Омлет с молоком']
    text = response().create(recipe_data)
    
    logger.info(f"Ответ сгенерирован в формате: {type}")
    return text

"""
Получить список всех рецептов в формате JSON
"""
@app.route("/api/recipes", methods=['GET'])
def get_recipes():
    logger.info("Запрос списка всех рецептов")
    try:
        recipes_data = data.get(reposity.recipe_key(), {})
        
        # Преобразуем все рецепты в JSON-совместимый формат
        converted_recipes = []
        for recipe_name, recipe in recipes_data.items():
            converted_recipe = converter.convert(recipe)
            converted_recipes.append(converted_recipe)
        
        logger.info(f"Возвращено {len(converted_recipes)} рецептов")
        return jsonify(converted_recipes)
        
    except Exception as e:
        logger.error(f"Ошибка при получении списка рецептов: {str(e)}")
        abort(500, description=f"Ошибка при получении списка рецептов: {str(e)}")

"""
Получить конкретный рецепт по ID в формате JSON
"""
@app.route("/api/recipes/<string:recipe_id>", methods=['GET'])
def get_recipe(recipe_id):
    logger.info(f"Запрос рецепта с ID: {recipe_id}")
    try:
        recipes_data = data.get(reposity.recipe_key(), {})
        
        # Ищем рецепт по ID
        found_recipe = None
        for recipe_name, recipe in recipes_data.items():
            # Предполагаем, что у рецепта есть поле 'id'
            if hasattr(recipe, 'unique_code') and getattr(recipe, 'unique_code', None) == recipe_id:
                found_recipe = recipe
                break
            # Альтернативный поиск по имени, если ID не найден
            elif recipe_name == recipe_id:
                found_recipe = recipe
                break
        
        if not found_recipe:
            logger.warning(f"Рецепт с ID '{recipe_id}' не найден")
            abort(404, description=f"Рецепт с ID '{recipe_id}' не найден")
        
        # Преобразуем рецепт в JSON-совместимый формат
        converted_recipe = converter.convert(found_recipe)
        
        logger.info(f"Рецепт с ID '{recipe_id}' успешно найден")
        return jsonify(converted_recipe)
        
    except Exception as e:
        logger.error(f"Ошибка при получении рецепта {recipe_id}: {str(e)}")
        abort(500, description=f"Ошибка при получении рецепта: {str(e)}")

"""
Получить список всех справочников в формате JSON
"""
@app.route("/api/references", methods=['GET'])
def get_references():
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
        
        logger.info(f"Возвращено {len(references_data)} справочников")
        return jsonify(references_data)
        
    except Exception as e:
        logger.error(f"Ошибка при получении справочников: {str(e)}")
        abort(500, description=f"Ошибка при получении справочников: {str(e)}")

"""
Получить конкретный справочник по имени в формате JSON
"""
@app.route("/api/references/<string:reference_name>", methods=['GET'])
def get_reference(reference_name):
    logger.info(f"Запрос справочника: {reference_name}")
    try:
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

@app.errorhandler(404)
def page_not_found(error):
    logger.error(f"Ошибка 404: {error}")
    return jsonify({"error": "Ресурс не найден.", "status": 404}), 404

@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"Ошибка 500: {error}")
    return jsonify({"error": f"Внутренняя ошибка сервера: {str(error)}", "status": 500}), 500

if __name__ == '__main__':
    data_service.start()
    data = data_service.repo.data
    logger.info("Сервис запущен на 0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080)