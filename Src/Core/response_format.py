class response_formats:
    """
    Класс-контейнер для хранения констант форматов данных.
    Предоставляет статические методы для получения строковых идентификаторов форматов.
    """
    
    @staticmethod
    def csv() -> str:
        """Возвращает строковый идентификатор формата CSV"""
        return "csv"
    
    @staticmethod
    def json() -> str:
        """Возвращает строковый идентификатор формата JSON"""
        return "json"
    
    @staticmethod
    def markdown() -> str:
        """Возвращает строковый идентификатор формата Markdown"""
        return "markdown"

    @staticmethod
    def xml() -> str:
        """Возвращает строковый идентификатор формата XML"""
        return "xml"