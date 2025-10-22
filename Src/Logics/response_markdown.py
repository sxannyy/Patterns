from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Models.recipe_model import recipe_model
from typing import Any, List

class response_markdown(abstract_response):
    """
    Класс для генерации ответа в формате Markdown на основе данных.
    Наследуется от abstract_response и реализует метод create для преобразования 
    данных в строку Markdown с использованием заголовков, таблиц и списков.
    """
    
    def create(self, data: Any):
        """
        Генерирует строку в формате Markdown на основе предоставленных данных.
        
        Параметры:
            data: Данные. Может быть одним объектом или списком объектов.
        
        Возвращает:
            str: Строка в формате Markdown. Для recipe_model включает заголовок рецепта, 
                 таблицу ингредиентов и нумерованный список шагов. Для других объектов
                 генерирует таблицу на основе их свойств.
        """
        
        # Если data не список, оборачиваем в список
        if not isinstance(data, list):
            data = [data]

        text = ""
        
        # Обрабатываем каждый элемент данных
        for item in data:
            # Если элемент - recipe_model, обрабатываем специально
            if isinstance(item, recipe_model):
                text += self.__format_recipe(item)
            else:
                text += self.__format_generic_object(item)
            
            # Добавляем разделитель между элементами (кроме последнего)
            if item != data[-1]:
                text += "\n---\n\n"
        
        return text
    
    def __format_recipe(self, recipe: recipe_model) -> str:
        """
        Форматирует рецепт в Markdown.
        
        Параметры:
            recipe: Объект recipe_model
            
        Возвращает:
            str: Отформатированный рецепт в Markdown
        """
        text = f"# {recipe.name}\n\n"

        # Добавляем раздел ингредиентов с таблицей
        text += "## Ингредиенты:\n"
        if recipe.ingredients:
            text += "| Ингредиент | Количество |\n"
            text += "|-------------|------------|\n"
            for ingredient in recipe.ingredients:
                nom_name = self.__get_object_name(ingredient[0])
                text += f"| {nom_name} | {ingredient[1]} |\n"
        else:
            text += "*Нет ингредиентов*\n"
        text += "\n"
        
        # Добавляем раздел шагов с нумерованным списком
        text += "## Шаги приготовления:\n"
        if recipe.steps:
            for i, step in enumerate(recipe.steps, 1):
                text += f"{i}. {step}\n"
        else:
            text += "*Нет шагов приготовления*\n"
        text += "\n"
        
        return text
    
    def __format_generic_object(self, obj: Any) -> str:
        """
        Форматирует произвольный объект в Markdown.
        
        Параметры:
            obj: Любой объект
            
        Возвращает:
            str: Отформатированный объект в Markdown
        """
        # Получаем свойства объекта
        properties = self.__get_properties(obj)
        
        # Если у объекта есть имя, используем его как заголовок
        object_name = self.__get_object_name(obj)
        if object_name and object_name != str(obj):
            text = f"# {object_name}\n\n"
        else:
            text = f"# Объект\n\n"
        
        # Создаем таблицу свойств
        if properties:
            text += "## Свойства:\n"
            text += "| Свойство | Значение |\n"
            text += "|----------|----------|\n"
            
            for prop in properties:
                value = getattr(obj, prop)
                formatted_value = self.__format_value(value)
                text += f"| {prop} | {formatted_value} |\n"
        else:
            text += "*Нет свойств для отображения*\n"
        
        return text
    
    def __get_properties(self, obj: Any) -> List[str]:
        """
        Получает список свойств объекта.
        
        Параметры:
            obj: Объект для анализа
            
        Возвращает:
            List[str]: Список имен свойств
        """
        properties = []
        
        # Для словаря используем ключи
        if isinstance(obj, dict):
            return list(obj.keys())
        
        # Для объектов получаем атрибуты
        for attr_name in dir(obj):
            # Пропускаем приватные атрибуты и методы
            if attr_name.startswith('_'):
                continue
                
            attr_value = getattr(obj, attr_name)
            # Пропускаем callable объекты (методы)
            if callable(attr_value):
                continue
                
            properties.append(attr_name)
        
        return properties
    
    def __get_object_name(self, obj: Any) -> str:
        """
        Получает читаемое имя объекта.
        
        Параметры:
            obj: Объект
            
        Возвращает:
            str: Имя объекта
        """
        if hasattr(obj, 'name'):
            return str(obj.name)
        elif hasattr(obj, 'title'):
            return str(obj.title)
        elif hasattr(obj, 'id'):
            return f"Объект {obj.id}"
        else:
            return str(obj)
    
    def __format_value(self, value: Any) -> str:
        """
        Форматирует значение для отображения в Markdown.
        
        Параметры:
            value: Значение для форматирования
            
        Возвращает:
            str: Отформатированное значение
        """
        if value is None:
            return "—"
        elif isinstance(value, list):
            if not value:
                return "—"
            # Для списков ингредиентов форматируем специально
            if all(isinstance(item, tuple) and len(item) == 2 for item in value):
                formatted_items = []
                for item in value:
                    nom_name = self._get_object_name(item[0])
                    formatted_items.append(f"{nom_name}: {item[1]}")
                return ", ".join(formatted_items)
            else:
                return ", ".join([str(item) for item in value])
        elif isinstance(value, dict):
            return ", ".join([f"{k}: {v}" for k, v in value.items()])
        else:
            return str(value)