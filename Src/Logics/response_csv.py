from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Models.recipe_model import recipe_model

class response_csv(abstract_response):
    """
    Класс для генерации ответа в формате CSV на основе данных рецепта.
    Наследуется от abstract_response и реализует метод create для преобразования 
    данных рецепта в строку CSV.
    """
    
    def create(self, data: recipe_model):
        """
        Генерирует строку в формате CSV на основе предоставленных данных рецепта.
        
        Параметры:
            data (recipe_model или list): Данные рецепта. Может быть одним объектом recipe_model 
                                         или списком таких объектов. Если список содержит dict'ы 
                                         или другие объекты, обрабатывается как общие данные.
        
        Возвращает:
            str: Строка в формате CSV, содержащая данные рецепта(ов). Включает заголовки 
                 и строки данных, с экранированием специальных символов (точки с запятой 
                 заменяются на запятые, кавычки на апострофы).
        
        Логика:
            - Если data не список, оборачивает в список.
            - Если элементы списка - recipe_model, строит CSV с колонками: Название, Ингредиенты, Шаги приготовления.
              Ингредиенты форматируются как "ингредиент: количество", шаги как "1. шаг | 2. шаг".
            - Если элементы - dict или другие объекты, определяет поля (ключи dict или ['name', 'ingredients', 'steps']) 
              и строит CSV на их основе.
        """
        
        # Проверяем, является ли data списком; если нет, делаем его списком для унификации обработки
        if not isinstance(data, list):
            data = [data]

        # Если первый элемент - recipe_model, обрабатываем как рецепты
        if isinstance(data[0], recipe_model):
            # Заголовок CSV для рецептов
            text = "Название;Ингредиенты;Шаги приготовления\n"
            
            # Проходим по каждому рецепту
            for recipe in data:
                # Форматируем ингредиенты: "ингредиент: количество" через запятую
                ingredients_str = ", ".join([
                    f"{ing[0].name if hasattr(ing[0], 'name') else str(ing[0])}: {ing[1]}"
                    for ing in recipe.ingredients
                ])

                # Форматируем шаги: "1. шаг | 2. шаг" и т.д.
                steps_str = " | ".join([f"{i+1}. {step}" for i, step in enumerate(recipe.steps)])

                # Экранируем специальные символы в строках (заменяем ; на ,, " на ')
                name_esc = str(recipe.name).replace(';', ',').replace('"', "'")
                ingredients_esc = ingredients_str.replace(';', ',').replace('"', "'")
                steps_esc = steps_str.replace(';', ',').replace('"', "'")
                
                # Добавляем строку в CSV
                text += f"{name_esc};{ingredients_esc};{steps_esc}\n"
        else:
            # Если не recipe_model, предполагаем dict или объекты с полями
            item = data[0]
            # Определяем поля: ключи dict или стандартные ['name', 'ingredients', 'steps']
            if isinstance(item, dict):
                fields = list(item.keys())
            else:
                fields = ['name', 'ingredients', 'steps']
            # Добавляем заголовок на основе полей
            for field in fields:
                text += f"{field};"
            text += "\n"
            # Проходим по данным и добавляем строки
            for d in data:
                for field in fields:
                    # Получаем значение: из dict или атрибута объекта
                    if isinstance(d, dict):
                        val = d.get(field, "")
                    else:
                        val = getattr(d, field, "")
                    # Экранируем специальные символы
                    val_esc = str(val).replace(';', ',').replace('"', "'")
                    text += f"{val_esc};"
                text += "\n"
        
        return text