from Src.Core.abstract_response import abstract_response
from xml.etree.ElementTree import Element, SubElement, tostring
from Src.Models.recipe_model import recipe_model
from typing import Any

class response_xml(abstract_response):
    """
    Класс для генерации XML-ответа на основе данных.
    Наследуется от абстрактного класса abstract_response.
    """

    def create(self, data: Any):
        """
        Создает XML-структуру на основе переданных данных.

        :param data: Один объект или список объектов.
        :return: Строка, представляющая XML-структуру.
        """
        
        # Если data не является списком, преобразуем его в список
        if not isinstance(data, list):
            data = [data]
        
        # Определяем корневой элемент на основе типа данных
        root_name = self.__get_root_element_name(data[0])
        root = Element(root_name)
        
        # Обрабатываем каждый элемент в data
        for item in data:
            if isinstance(item, recipe_model):
                self.__add_recipe_element(root, item)
            else:
                self.__add_generic_element(root, item)
        
        # Генерируем XML
        xml_content = tostring(root, encoding='unicode')
        
        # Добавляем XML-заголовок
        xml_head = '<?xml version="1.0" encoding="UTF-8"?>'
        return xml_head + '\n' + xml_content
    
    def __get_root_element_name(self, first_item: Any) -> str:
        """
        Определяет имя корневого элемента на основе типа данных.
        
        :param first_item: Первый элемент данных
        :return: Имя корневого элемента
        """
        if isinstance(first_item, recipe_model):
            return 'recipes'
        elif hasattr(first_item, '__class__'):
            class_name = first_item.__class__.__name__.lower()
            # Убираем суффикс '_model' если есть
            if class_name.endswith('_model'):
                class_name = class_name[:-6]
            return class_name + 's'  # Множественное число
        else:
            return 'items'
    
    def __add_recipe_element(self, root: Element, recipe: recipe_model):
        """
        Добавляет элемент рецепта в XML.
        
        :param root: Корневой элемент
        :param recipe: Объект рецепта
        """
        recipe_elem = SubElement(root, 'recipe')
        
        # Добавляем название рецепта
        name_elem = SubElement(recipe_elem, 'name')
        name_elem.text = str(recipe.name)
        
        # Добавляем ингредиенты рецепта
        ingredients_elem = SubElement(recipe_elem, 'ingredients')
        for ingredient in recipe.ingredients:
            ing_elem = SubElement(ingredients_elem, 'ingredient')
            
            # Добавляем номенклатуру ингредиента
            nom_elem = SubElement(ing_elem, 'nomenclature')
            nom_name = self.__get_object_name(ingredient[0])
            nom_elem.text = nom_name
            
            # Добавляем количество ингредиента
            qty_elem = SubElement(ing_elem, 'quantity')
            qty_elem.text = str(ingredient[1])
        
        # Добавляем шаги приготовления рецепта
        steps_elem = SubElement(recipe_elem, 'steps')
        for i, step in enumerate(recipe.steps):
            step_elem = SubElement(steps_elem, 'step')
            step_elem.set('number', str(i+1))
            step_elem.text = step
    
    def __add_generic_element(self, root: Element, item: Any):
        """
        Добавляет произвольный объект в XML.
        
        :param root: Корневой элемент
        :param item: Объект для добавления
        """
        # Определяем имя элемента
        if hasattr(item, '__class__'):
            elem_name = item.__class__.__name__.lower()
            if elem_name.endswith('_model'):
                elem_name = elem_name[:-6]
        else:
            elem_name = 'item'
        
        item_elem = SubElement(root, elem_name)
        
        # Получаем свойства объекта
        properties = self.__get_object_properties(item)
        
        # Добавляем свойства как дочерние элементы
        for key, value in properties.items():
            self.__add_property_element(item_elem, key, value)
    
    def __get_object_properties(self, obj: Any) -> dict:
        """
        Получает свойства объекта в виде словаря.
        
        :param obj: Объект для анализа
        :return: Словарь свойств
        """
        if hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):
            return obj.dict()
        elif hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            return obj.to_dict()
        elif isinstance(obj, dict):
            return obj
        elif hasattr(obj, '__dict__'):
            # Фильтруем приватные атрибуты и методы
            properties = {}
            for key, value in obj.__dict__.items():
                if not key.startswith('_') and not callable(value):
                    properties[key] = value
            return properties
        else:
            # Для простых типов или итерируемых объектов
            return {'value': str(obj)}
    
    def __add_property_element(self, parent: Element, key: str, value: Any):
        """
        Добавляет свойство как дочерний элемент.
        
        :param parent: Родительский элемент
        :param key: Ключ свойства
        :param value: Значение свойства
        """
        prop_elem = SubElement(parent, key)
        
        if isinstance(value, list):
            # Обрабатываем списки
            for i, item in enumerate(value):
                if isinstance(item, (dict, object)) and not isinstance(item, (str, int, float)):
                    # Для сложных объектов в списке
                    list_elem = SubElement(prop_elem, 'item')
                    list_elem.set('index', str(i))
                    item_properties = self.__get_object_properties(item)
                    for k, v in item_properties.items():
                        self.__add_property_element(list_elem, k, v)
                else:
                    # Для простых значений в списке
                    item_elem = SubElement(prop_elem, 'item')
                    item_elem.set('index', str(i))
                    item_elem.text = str(item)
        elif isinstance(value, dict):
            # Обрабатываем словари
            for k, v in value.items():
                self.__add_property_element(prop_elem, str(k), v)
        elif hasattr(value, '__dict__') or hasattr(value, 'dict') or hasattr(value, 'to_dict'):
            # Обрабатываем вложенные объекты
            nested_properties = self.__get_object_properties(value)
            for k, v in nested_properties.items():
                self.__add_property_element(prop_elem, k, v)
        else:
            # Простые значения
            prop_elem.text = str(value)
    
    def __get_object_name(self, obj: Any) -> str:
        """
        Получает читаемое имя объекта.
        
        :param obj: Объект
        :return: Имя объекта
        """
        if hasattr(obj, 'name'):
            return str(obj.name)
        elif hasattr(obj, 'title'):
            return str(obj.title)
        else:
            return str(obj)