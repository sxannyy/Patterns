from Src.Core.abstract_response import abstract_response
from typing import Any

class response_csv(abstract_response):

    """
    Класс для генерации ответа в формате CSV на основе данных.
    Использует convert_factory для преобразования объектов в словари.
    """
    
    # Разделитель CSV
    delimiter: str = ";"
    
    def create(self, data: Any) -> str:

        """
        Генерирует строку в формате CSV на основе предоставленных данных.
        """
        
        # Если data не список, оборачиваем в список
        if not isinstance(data, list):
            data = [data]

        # Преобразуем все данные через convert_factory
        converted_data = self._converter.convert_list(data)
        
        if not converted_data:
            return ""
            
        # Получаем все возможные заголовки из всех объектов
        all_headers = set()
        for item in converted_data:
            all_headers.update(item.keys())
        
        # Убираем служебные поля
        all_headers = [h for h in all_headers if h not in ['converter', 'type']]
        headers = sorted(all_headers)
        
        # Создаем заголовок CSV
        text = self.delimiter.join(headers) + "\n"
        
        # Добавляем строки с данными
        rows = []
        for item in converted_data:
            values = []
            for header in headers:
                value = item.get(header, "")
                values.append(self.__format_csv_value(value))
            rows.append(self.delimiter.join(values))
        
        text += "\n".join(rows)
        return text
    
    def __format_csv_value(self, value: Any) -> str:
        """
        Форматирует значение для CSV.
        """
        if value is None:
            return ""
        
        str_value = str(value)
        
        # Экранируем специальные символы
        str_value = str_value.replace(self.delimiter, ',').replace('"', "'")
        
        # Если строка содержит разделитель или переносы строк, обрамляем в кавычки
        if self.delimiter in str_value or '\n' in str_value or '\r' in str_value:
            str_value = f'"{str_value}"'
            
        return str_value