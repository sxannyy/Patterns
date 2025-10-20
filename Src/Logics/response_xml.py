from Src.Core.abstract_response import abstract_response
from xml.etree.ElementTree import Element, SubElement, tostring
from Src.Models.recipe_model import recipe_model

class response_xml(abstract_response):
    """
    Класс для генерации XML-ответа на основе модели рецепта.
    Наследуется от абстрактного класса abstract_response.
    """

    def create(self, data: recipe_model):
        """
        Создает XML-структуру на основе переданных данных о рецепте.

        :param data: Один объект recipe_model или список объектов recipe_model.
        :return: Строка, представляющая XML-структуру.
        """
        
        # Если data не является списком, преобразуем его в список
        if not isinstance(data, list):
            data = [data]
        
        # Создаем корневой элемент 'recipes'
        root = Element('recipes')
        
        # Обрабатываем каждый элемент в data
        for item in data:
            # Проверяем, является ли элемент экземпляром recipe_model
            if isinstance(item, recipe_model):
                # Создаем элемент 'recipe' для каждого рецепта
                recipe_elem = SubElement(root, 'recipe')
                
                # Добавляем название рецепта
                name_elem = SubElement(recipe_elem, 'name')
                name_elem.text = str(item.name)
                
                # Добавляем ингредиенты рецепта
                ingredients_elem = SubElement(recipe_elem, 'ingredients')
                for ingredient in item.ingredients:
                    ing_elem = SubElement(ingredients_elem, 'ingredient')
                    
                    # Добавляем номенклатуру ингредиента
                    nom_elem = SubElement(ing_elem, 'nomenclature')
                    nom_name = ingredient[0].name if hasattr(ingredient[0], 'name') else str(ingredient[0])
                    nom_elem.text = nom_name
                    
                    # Добавляем количество ингредиента
                    qty_elem = SubElement(ing_elem, 'quantity')
                    qty_elem.text = str(ingredient[1])
                
                # Добавляем шаги приготовления рецепта
                steps_elem = SubElement(recipe_elem, 'steps')
                for i, step in enumerate(item.steps):
                    step_elem = SubElement(steps_elem, 'step')
                    step_elem.set('number', str(i+1))  # Устанавливаем номер шага
                    step_elem.text = step  # Добавляем текст шага
            
            else:
                # Если элемент не является recipe_model, обрабатываем его как обычный объект
                it = SubElement(root, 'item')
                if hasattr(item, 'dict'):
                    src = item.dict  # Получаем словарь из объекта
                elif isinstance(item, dict):
                    src = item  # Если это уже словарь, просто используем его
                else:
                    # В противном случае создаем словарь из атрибутов объекта
                    src = {k: getattr(item, k) for k in dir(item) if not k.startswith('_') and not callable(getattr(item, k))}
                
                # Добавляем элементы для каждого ключа и значения в словаре
                for k, v in src.items():
                    child = SubElement(it, str(k))
                    child.text = str(v)
        
        # Возвращаем строку XML-структуры
        return tostring(root, encoding='unicode')
