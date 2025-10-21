from Src.Core.abstract_response import abstract_response
from Src.Models.recipe_model import recipe_model
import json
from typing import Any

class response_json(abstract_response):
    """
    Класс для генерации ответа в формате JSON на основе данных.
    Наследуется от abstract_response и реализует метод create для преобразования 
    данных в строку JSON.
    """
    
    def create(self, data: Any):
        """
        Генерирует строку в формате JSON на основе предоставленных данных.
        
        Параметры:
            data: Данные. Может быть одним объектом или списком объектов.
        
        Возвращает:
            str: Строка в формате JSON, содержащая данные.
        """
        
        # Если data не список, оборачиваем в список
        if not isinstance(data, list):
            data = [data]
    
        # Список для хранения JSON-совместимых данных
        json_compatible_data = []
        
        # Проходим по каждому элементу данных
        for item in data:
            json_compatible_data.append(self.__convert_to_dict(item))
        
        # Возвращаем JSON-строку с отступами и поддержкой не-ASCII символов
        return json.dumps(json_compatible_data, ensure_ascii=False, indent=2)
    
    def __convert_to_dict(self, obj: Any) -> dict:
        """
        Конвертирует объект в словарь для JSON-сериализации.
        
        Параметры:
            obj: Объект для конвертации
            
        Возвращает:
            dict: Словарь с данными объекта
        """
        try:
            # Если объект - recipe_model, обрабатываем специально
            if isinstance(obj, recipe_model):
                return self.__convert_recipe_model(obj)
            
            # Если объект имеет метод to_dict, используем его
            elif hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
                return obj.to_dict()
            
            # Если объект имеет метод dict, используем его
            elif hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):
                return obj.dict()
            
            # Если объект имеет __dict__, используем его
            elif hasattr(obj, '__dict__'):
                result = {}
                for key, value in obj.__dict__.items():
                    # Пропускаем приватные атрибуты
                    if key.startswith('_'):
                        continue
                    result[key] = self.__process_value(value)
                return result
            
            # Иначе пытаемся конвертировать в dict напрямую
            else:
                return dict(obj)
                
        except (TypeError, ValueError, AttributeError):
            # В случае ошибок конвертируем в строку
            return str(obj)
    
    def __convert_recipe_model(self, recipe: recipe_model) -> dict:
        """
        Конвертирует recipe_model в словарь.
        
        Параметры:
            recipe: Объект recipe_model
            
        Возвращает:
            dict: Словарь с данными рецепта
        """
        return {
            'name': recipe.name,
            'ingredients': [
                {
                    'nomenclature': self.__process_nomenclature(ing[0]),
                    'quantity': ing[1]
                } for ing in recipe.ingredients
            ],
            'steps': recipe.steps
        }
    
    def __process_nomenclature(self, nomenclature: Any) -> Any:
        """
        Обрабатывает номенклатуру для JSON-сериализации.
        
        Параметры:
            nomenclature: Объект номенклатуры
            
        Возвращает:
            Любой JSON-совместимый объект
        """
        if hasattr(nomenclature, 'name'):
            return nomenclature.name
        elif hasattr(nomenclature, '__dict__'):
            # Рекурсивно конвертируем объект номенклатуры
            return self.__convert_to_dict(nomenclature)
        else:
            return str(nomenclature)
    
    def __process_value(self, value: Any) -> Any:
        """
        Рекурсивно обрабатывает значения для JSON-сериализации.
        
        Параметры:
            value: Значение для обработки
            
        Возвращает:
            JSON-совместимое значение
        """
        if value is None:
            return None
        elif isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, list):
            return [self.__process_value(item) for item in value]
        elif isinstance(value, dict):
            return {str(k): self.__process_value(v) for k, v in value.items()}
        elif hasattr(value, '__dict__'):
            return self.__convert_to_dict(value)
        else:
            return str(value)