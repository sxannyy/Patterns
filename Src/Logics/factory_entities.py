from Src.Core.abstract_response import abstract_response
from Src.Logics.response_csv import response_csv
from Src.Logics.response_json import response_json
from Src.Logics.response_markdown import response_markdown
from Src.Logics.response_xml import response_xml
from Src.Core.validator import operation_exception
from Src.Core.response_format import response_formats
from Src.Models.settings_model import settings_model

class factory_entities:

    """
    Фабрика для создания объектов ответов в различных форматах (CSV, JSON, Markdown, XML).
    Используется для унификации создания ответов на основе заданного формата.
    """
    
    # Словарь, сопоставляющий ключи форматов (из response_formats) с соответствующими классами ответов
    __match = {
        response_formats.csv(): response_csv,
        response_formats.json(): response_json,
        response_formats.markdown(): response_markdown,
        response_formats.xml(): response_xml
    }
    
    @property
    def response_formats(self) -> dict:

        """
        Свойство, возвращающее словарь доступных форматов ответов.
        Возвращает:
            dict: Словарь, где ключи - строки форматов (например, 'csv', 'json'), 
                  значения - классы ответов (например, response_csv, response_json).
        """

        return self.__match
        
    def create(self, format: str) -> abstract_response:

        """
        Создает объект ответа на основе заданного формата.
        Параметры:
            format (str): Строка, представляющая формат ответа (например, 'json', 'xml').
                          Должна быть ключом в словаре __match.
        Возвращает:
            abstract_response: Экземпляр класса ответа, соответствующего формату 
                              (наследуется от abstract_response).
        Вызывает:
            operation_exception: Если указанный формат не найден в __match.
        """

        if format not in self.__match.keys():
            raise operation_exception("Формат неверный!")
        return self.__match[format]

    def create_default(self, settings: settings_model):

        """
        Создает объект ответа по умолчанию на основе настроек.
        Параметры:
            settings (settings_model): Объект настроек, содержащий информацию о формате ответа.
                                      Должен иметь атрибут response_format.
        Возвращает:
            abstract_response: Экземпляр класса ответа, соответствующего формату из настроек.
        Вызывает:
            operation_exception: Если settings равен None или формат в настройках неверный.
        """
        
        if settings is None:
            raise operation_exception("Настройки не представлены в FactoryEntities!")
        fmt = settings.response_format
        responder = self.create(fmt)
        return responder