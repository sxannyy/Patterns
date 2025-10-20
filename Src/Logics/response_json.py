from Src.Core.abstract_response import abstract_response
from Src.Models.recipe_model import recipe_model
import json

class response_json(abstract_response):
    """
    Класс для генерации ответа в формате JSON на основе данных рецепта.
    Наследуется от abstract_response и реализует метод create для преобразования 
    данных рецепта в строку JSON.
    """
    
    def create(self, data: recipe_model):
        """
        Генерирует строку в формате JSON на основе предоставленных данных рецепта.
        
        Параметры:
            data (recipe_model или list): Данные рецепта. Может быть одним объектом recipe_model 
                                         или списком таких объектов. Поддерживает также другие типы 
                                         данных с методами to_dict, dict или с __dict__.
        
        Возвращает:
            str: Строка в формате JSON, содержащая данные рецепта(ов). Для recipe_model 
                 включает поля 'name', 'ingredients' (как список словарей с 'nomenclature' и 'quantity') 
                 и 'steps'. Для других объектов пытается конвертировать в dict. 
                 Использует ensure_ascii=False для поддержки кириллицы и indent=2 для читаемости.
        
        Логика:
            - Если data не список, оборачивает в список.
            - Для каждого элемента пытается преобразовать в JSON-совместимый словарь:
              - Для recipe_model строит словарь с именованными полями.
              - Для объектов с to_dict() или dict() вызывает эти методы.
              - Для объектов с __dict__ использует его.
              - Для dict'ов или итерируемых объектов пытается конвертировать напрямую.
              - В случае ошибок конвертирует элемент в строку.
            - Возвращает JSON-строку с отступами и без экранирования ASCII.
        """
        
        # Проверяем, является ли data списком; если нет, делаем его списком для унификации обработки
        if not isinstance(data, list):
            data = [data]
    
        # Список для хранения JSON-совместимых данных
        json_compatible_data = []
        
        # Проходим по каждому элементу данных
        for item in data:
            try:
                # Если элемент - recipe_model, строим словарь вручную
                if isinstance(item, recipe_model):
                    recipe_dict = {
                        'name': item.name,
                        'ingredients': [
                            {
                                'nomenclature': ing[0].name if hasattr(ing[0], 'name') else str(ing[0]),
                                'quantity': ing[1]
                            } for ing in item.ingredients
                        ],
                        'steps': item.steps
                    }
                    json_compatible_data.append(recipe_dict)
                # Если объект имеет метод to_dict (например, pydantic модели), используем его
                elif hasattr(item, 'to_dict') and callable(getattr(item, 'to_dict')):
                    json_compatible_data.append(item.to_dict())
                # Если объект имеет метод dict (pydantic), используем его
                elif hasattr(item, 'dict') and callable(getattr(item, 'dict')):
                    json_compatible_data.append(item.dict())
                # Если объект имеет __dict__, используем его
                elif hasattr(item, '__dict__'):
                    json_compatible_data.append(item.__dict__)
                # Иначе пытаемся конвертировать в dict напрямую (для dict'ов или итерируемых)
                else:
                    json_compatible_data.append(dict(item))
            # В случае ошибок (TypeError, ValueError) конвертируем в строку
            except (TypeError, ValueError):
                json_compatible_data.append(str(item))
        
        # Возвращаем JSON-строку с отступами и поддержкой не-ASCII символов
        return json.dumps(json_compatible_data, ensure_ascii=False, indent=2)