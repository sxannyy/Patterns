from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Models.recipe_model import recipe_model
from typing import List, Any

class response_csv(abstract_response):
    """
    Класс для генерации ответа в формате CSV на основе данных.
    Наследуется от abstract_response и реализует метод create для преобразования 
    данных в строку CSV.
    """
    
    # Разделитель CSV
    delimiter: str = ";"
    
    def create(self, data: Any):
        """
        Генерирует строку в формате CSV на основе предоставленных данных.
        
        Параметры:
            data: Данные. Может быть одним объектом или списком объектов.
        
        Возвращает:
            str: Строка в формате CSV, содержащая данные с заголовками.
        """
        
        # Если data не список, оборачиваем в список
        if not isinstance(data, list):
            data = [data]

        # Получаем свойства первого объекта для создания заголовка
        item = data[0]
        properties = self.__get_properties(item)
        
        # Создаем заголовок CSV
        text = self.delimiter.join(properties) + "\n"
        
        # Добавляем строки с данными
        rows = []
        for item in data:
            values = []
            for prop in properties:
                value = getattr(item, prop)
                # Специальная обработка для ingredients
                if prop == 'ingredients':
                    values.append(self.__format_ingredients(value))
                else:
                    values.append(self.__obj_to_str(value))
            
            rows.append(self.delimiter.join(values))
        
        text += "\n".join(rows)
        return text
    
    def __format_ingredients(self, ingredients: list) -> str:
        """
        Форматирует список ингредиентов в читаемую строку.
        
        Параметры:
            ingredients: Список кортежей (номенклатура, количество)
            
        Возвращает:
            str: Отформатированная строка ингредиентов
        """
        formatted_ingredients = []
        for ing in ingredients:
            nomenclature, quantity = ing
            # Получаем название номенклатуры
            if hasattr(nomenclature, 'name'):
                ing_name = nomenclature.name
            else:
                ing_name = str(nomenclature)
            formatted_ingredients.append(f"{ing_name}: {quantity}")
        
        return ", ".join(formatted_ingredients)
    
    def __get_properties(self, obj: Any) -> List[str]:
        """
        Получает список свойств объекта, исключая приватные и служебные методы.
        
        Параметры:
            obj: Объект для анализа
            
        Возвращает:
            List[str]: Список имен свойств
        """
        properties = []
        exclude_props = ['unique_code']  # Свойства, которые нужно исключить, исключаем UUID
        
        for attr_name in dir(obj):
            # Пропускаем приватные атрибуты и методы
            if attr_name.startswith('_'):
                continue
                
            # Пропускаем исключенные свойства
            if attr_name in exclude_props:
                continue
                
            attr_value = getattr(obj, attr_name)
            # Пропускаем callable объекты (методы)
            if callable(attr_value):
                continue
                
            properties.append(attr_name)
        
        return properties
    
    def __obj_to_str(self, obj: Any) -> str:
        """
        Преобразует объект в строку с экранированием специальных символов.
        
        Параметры:
            obj: Объект для преобразования
            
        Возвращает:
            str: Строковое представление объекта
        """
        if obj is None:
            return ""
        
        # Обработка списков (например, steps)
        if isinstance(obj, list):
            # Для шагов рецепта форматируем как пронумерованный список
            if all(isinstance(item, str) for item in obj):
                formatted_steps = []
                for i, step in enumerate(obj, 1):
                    formatted_steps.append(f"{i}. {step}")
                str_value = " | ".join(formatted_steps)
            else:
                str_value = ", ".join([str(item) for item in obj])
        else:
            str_value = str(obj)
        
        # Экранируем специальные символы
        str_value = str_value.replace(self.delimiter, ',').replace('"', "'")
        
        # Если строка содержит разделитель или переносы строк, обрамляем в кавычки
        if self.delimiter in str_value or '\n' in str_value or '\r' in str_value:
            str_value = f'"{str_value}"'
            
        return str_value