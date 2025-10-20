from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Models.recipe_model import recipe_model

class response_markdown(abstract_response):
    """
    Класс для генерации ответа в формате Markdown на основе данных рецепта.
    Наследуется от abstract_response и реализует метод create для преобразования 
    данных рецепта в строку Markdown с использованием заголовков, таблиц и списков.
    """
    
    def create(self, data: recipe_model):
        """
        Генерирует строку в формате Markdown на основе предоставленных данных рецепта.
        
        Параметры:
            data (recipe_model или list): Данные рецепта. Может быть одним объектом recipe_model 
                                         или списком таких объектов. Поддерживает также другие типы 
                                         данных (dict или объекты с атрибутами).
        
        Возвращает:
            str: Строка в формате Markdown. Для recipe_model включает заголовок рецепта, 
                 таблицу ингредиентов и нумерованный список шагов. Для других данных 
                 генерирует таблицу на основе полей (ключей dict или стандартных атрибутов).
        
        Логика:
            - Если data не список, оборачивает в список для унификации.
            - Если элементы - recipe_model, строит Markdown с:
              - Заголовком (# Название рецепта).
              - Таблицей ингредиентов (с колонками "Ингредиент" и "Количество").
              - Нумерованным списком шагов приготовления.
              - Разделителем (---) между рецептами.
            - Если элементы - dict или объекты, определяет поля (ключи dict или ['name', 'ingredients', 'steps']) 
              и строит таблицу Markdown с заголовками и строками данных.
        """
        
        # Проверяем, является ли data списком; если нет, делаем его списком для унификации обработки
        if not isinstance(data, list):
            data = [data]

        # Если первый элемент - recipe_model, обрабатываем как рецепты
        if isinstance(data[0], recipe_model):
            text = ""
            # Проходим по каждому рецепту
            for recipe in data:
                # Добавляем заголовок рецепта
                text += f"# {recipe.name}\n\n"

                # Добавляем раздел ингредиентов с таблицей
                text += "## Ингредиенты:\n"
                text += "| Ингредиент | Количество |\n"
                text += "|-------------|------------|\n"
                for ingredient in recipe.ingredients:
                    # Получаем название ингредиента (из атрибута name или как строку)
                    nom_name = ingredient[0].name if hasattr(ingredient[0], 'name') else str(ingredient[0])
                    text += f"| {nom_name} | {ingredient[1]} |\n"
                text += "\n"
                
                # Добавляем раздел шагов с нумерованным списком
                text += "## Шаги приготовления:\n"
                for i, step in enumerate(recipe.steps, 1):
                    text += f"{i}. {step}\n"
                text += "\n---\n\n"  # Разделитель между рецептами
        else:
            # Если не recipe_model, предполагаем dict или объекты с полями
            # Определяем поля: ключи dict или стандартные ['name', 'ingredients', 'steps']
            if isinstance(data[0], dict):
                fields = list(data[0].keys())
            else:
                fields = ['name', 'ingredients', 'steps']
            
            # Строим заголовок таблицы
            header = "| " + " | ".join(fields) + " |\n"
            # Строим разделитель таблицы
            sep = "| " + " | ".join(['---'] * len(fields)) + " |\n"
            text = header + sep
            # Проходим по данным и добавляем строки таблицы
            for item in data:
                row = []
                for f in fields:
                    # Получаем значение: из атрибута объекта или из dict
                    val = getattr(item, f, None)
                    if val is None and isinstance(item, dict):
                        val = item.get(f, "")
                    row.append(str(val))
                text += "| " + " | ".join(row) + " |\n"
        
        return text