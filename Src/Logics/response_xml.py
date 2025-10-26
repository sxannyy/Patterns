from Src.Core.abstract_response import abstract_response
from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Any

class response_xml(abstract_response):

    """
    Класс для генерации XML-ответа на основе данных.
    Использует convert_factory для преобразования объектов в словари.
    """

    def create(self, data: Any) -> str:

        """ Создает XML-структуру на основе переданных данных """
        
        # Если data не является списком, преобразуем его в список
        if not isinstance(data, list):
            data = [data]
        
        # Определяем корневой элемент на основе типа данных
        root_name = self.__get_root_element_name(data[0])
        root = Element(root_name)
        
        # Обрабатываем каждый элемент в data через convert_factory
        for item in data:
            converted_item = self._converter.convert(item)
            self.__add_converted_element(root, converted_item)
        
        # Генерируем XML
        xml_content = tostring(root, encoding='unicode')
        
        # Добавляем XML-заголовок
        xml_head = '<?xml version="1.0" encoding="UTF-8"?>'
        return xml_head + '\n' + xml_content
    
    def __get_root_element_name(self, first_item: Any) -> str:

        """
        Определяет имя корневого элемента на основе типа данных
        """

        if hasattr(first_item, '__class__'):
            class_name = first_item.__class__.__name__.lower()
            if class_name.endswith('_model'):
                class_name = class_name[:-6]
            return class_name + 's'
        else:
            return 'items'
    
    def __add_converted_element(self, root: Element, converted_data: dict):

        """
        Добавляет преобразованные данные в XML
        """

        if 'type' in converted_data:
            elem_name = converted_data.get('type', 'item')
        else:
            elem_name = 'item'
        
        item_elem = SubElement(root, elem_name)
        self.__add_dict_to_xml(item_elem, converted_data)
    
    def __add_dict_to_xml(self, parent: Element, data: dict):

        """
        Рекурсивно добавляет словарь в XML
        """
        for key, value in data.items():
            # Пропускаем служебные поля
            if key in ['converter', 'type']:
                continue
                
            if isinstance(value, dict):
                sub_elem = SubElement(parent, key)
                self.__add_dict_to_xml(sub_elem, value)
            elif isinstance(value, list):
                list_elem = SubElement(parent, key)
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        item_elem = SubElement(list_elem, 'item')
                        item_elem.set('index', str(i))
                        self.__add_dict_to_xml(item_elem, item)
                    else:
                        item_elem = SubElement(list_elem, 'item')
                        item_elem.set('index', str(i))
                        item_elem.text = str(item)
            else:
                elem = SubElement(parent, key)
                elem.text = str(value)