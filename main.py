import connexion
from flask import abort, jsonify
import logging

from Src.Logics.factory_entities import factory_entities
from Src.reposity import reposity
from Src.start_service import start_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

flask_app = connexion.FlaskApp(__name__)
app = flask_app.app
data_service = start_service()
data = None
responses_factory = factory_entities()

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

@app.errorhandler(404)
def page_not_found(error):
    logger.error(f"Ошибка 404: {error}")
    return jsonify({"error": "Такого формата не найдено.", "status": 404}), 404

@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"Ошибка 500: {error}")
    return jsonify({"error": f"Внутренняя ошибка сервера: {str(error)}", "status": 500}), 500

if __name__ == '__main__':
    data_service.start()
    data = data_service.repo.data
    logger.info("Сервис запущен на 0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080)