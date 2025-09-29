# Исключение при проверки аргумента
class argument_exception(Exception):
    pass     

# Исключение при выполнении бизнес операции
class operation_exception(Exception):
    pass    

# Набор проверок данных
class validator:

    """
    Сервис валидации входных данных.

    Назначение:
        - Проверка значений на тип, пустоту и максимальную длину.
    Использование:
        validator.validate(value, expected_type, max_len)
    """

    @staticmethod
    def validate(value, type_, len_= None):
        
        """
            Валидация аргумента по типу и длине
        Args:
            value (any): Аргумент
            type_ (object): Ожидаемый тип
            len_ (int): Максимальная длина
        Raises:
            arguent_exception: Некорректный тип
            arguent_exception: Нулевая длина
            arguent_exception: Некорректная длина аргумента
        Returns:
            True или Exception
        """

        if value is None:
            raise argument_exception("Пустой аргумент")

        # Проверка типа
        if not isinstance(value, type_):
            raise argument_exception(f"Некорректный тип!\nОжидается {type_}. Текущий тип {type(value)}")

        # Проверка аргумента
        if len(str(value).strip()) == 0:
            raise argument_exception("Пустой аргумент")

        if len_ is not None and len(str(value).strip()) > len_:
            raise argument_exception("Некорректная длина аргумента")

        return True