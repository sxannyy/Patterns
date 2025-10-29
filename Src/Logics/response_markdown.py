from Src.Core.abstract_response import abstract_response
from typing import Any

class response_markdown(abstract_response):

    """
    Класс для генерации ответа в формате Markdown на основе данных.
    Использует convert_factory для преобразования объектов в словари.
    """
    
    def create(self, data: Any) -> str:

        """
        Генерирует строку в формате Markdown на основе предоставленных данных.
        """
        
        # Если data не список, оборачиваем в список
        if not isinstance(data, list):
            data = [data]

        text = ""
        
        # Обрабатываем каждый элемент данных через convert_factory
        for item in data:
            converted_item = self._converter.convert(item)
            text += self.__format_converted_data(converted_item)
            
            if item != data[-1]:
                text += "\n---\n\n"
        
        return text
    
    def __format_converted_data(self, data: dict) -> str:

        """
        Форматирует преобразованные данные в Markdown.
        """

        text = ""
        
        # Определяем заголовок
        if 'name' in data:
            text += f"# {data['name']}\n\n"
        elif 'class_name' in data:
            text += f"# {data['class_name']}\n\n"
        else:
            text += "# Данные\n\n"
        
        # Форматируем поля
        text += "## Свойства:\n"
        text += "| Свойство | Значение |\n"
        text += "|----------|----------|\n"
        
        for key, value in data.items():
            if key not in ['converter', 'type', 'class_name']:
                formatted_value = self.__format_value(value)
                text += f"| {key} | {formatted_value} |\n"
        
        return text
    
    def __format_value(self, value: Any) -> str:
        """
        Форматирует значение для отображения в Markdown.
        """
        if value is None:
            return "—"
        elif isinstance(value, (str, int, float, bool)):
            return str(value)
        elif isinstance(value, list):
            if not value:
                return "—"
            return ", ".join([self.__format_value(item) for item in value])
        elif isinstance(value, dict):
            return "{" + ", ".join([f"{k}: {self.__format_value(v)}" for k, v in value.items()]) + "}"
        else:
            return str(value)