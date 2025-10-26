from Src.Core.abstract_response import abstract_response
import json
from typing import Any

class response_json(abstract_response):

    """
    Класс для генерации ответа в формате JSON на основе данных.
    Использует convert_factory для преобразования объектов в словари.
    """
    
    def create(self, data: Any) -> str:
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
    
        # Используем convert_factory для преобразования данных
        json_compatible_data = self._converter.convert_list(data)
        
        # Возвращаем JSON-строку с отступами
        return json.dumps(json_compatible_data, ensure_ascii=False, indent=2)