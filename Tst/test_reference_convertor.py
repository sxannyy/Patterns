import unittest
from datetime import datetime, date, time
from Src.Convertors.reference_convertor import reference_convertor
from Src.Core.abstract_model import abstract_model
from Src.Core.abstract_dto import abstract_dto
from Src.Core.common import common

"""
    Unit-тесты для модуля reference_convertor:
    Проверяется:
    - Преобразование объектов abstract_model и abstract_dto
    - Проверка возможности конвертации различных типов
    - Обработка неподдерживаемых типов
"""

class TestReferenceModel(abstract_model):
    def __init__(self, name: str = "test"):
        super().__init__(name)
        self.test_field = "test_value"
    
    def to_dto(self):
        """Реализация метода to_dto для тестовой модели"""
        return {
            "name": self.name,
            "test_field": self.test_field,
            "unique_code": self.unique_code
        }

class TestReferenceDTO(abstract_dto):
    def __init__(self):
        super().__init__()
        self.dto_field = "dto_value"
    
    def to_dto(self):
        """Реализация метода to_dto для тестового DTO"""
        return {
            "dto_field": self.dto_field,
            "id": self.id
        }

class TestReferenceConvertor(unittest.TestCase):

    def setUp(self):
        self.convertor = reference_convertor()

    def test_can_convert_abstract_model(self):
        # Подготовка
        model = TestReferenceModel()

        # Действие
        result = self.convertor.can_convert(model)

        # Проверка
        self.assertTrue(result)

    def test_can_convert_abstract_dto(self):
        # Подготовка
        dto = TestReferenceDTO()

        # Действие
        result = self.convertor.can_convert(dto)

        # Проверка
        self.assertTrue(result)

    def test_can_convert_regular_object(self):
        # Подготовка
        class RegularClass:
            def __init__(self):
                self.field = "value"

        obj = RegularClass()

        # Действие
        result = self.convertor.can_convert(obj)

        # Проверка
        self.assertTrue(result)

    def test_cannot_convert_basic_types(self):
        # Подготовка
        test_cases = ["string", 123, 45.67, True, None]

        # Действие и проверка
        for test_case in test_cases:
            result = self.convertor.can_convert(test_case)
            self.assertFalse(result, f"Не должен конвертировать тип: {type(test_case)}")

    def test_cannot_convert_type_class(self):
        # Подготовка
        class_type = TestReferenceModel

        # Действие
        result = self.convertor.can_convert(class_type)

        # Проверка
        self.assertFalse(result)

    def test_convert_abstract_model(self):
        # Подготовка
        model = TestReferenceModel("test_model")

        # Действие
        result = self.convertor.convert(model)

        # Проверка
        self.assertIsInstance(result, dict)
        self.assertIn("name", result)
        self.assertEqual(result["name"], "test_model")
        self.assertIn("test_field", result)
        self.assertEqual(result["test_field"], "test_value")
        self.assertIn("unique_code", result)

    def test_convert_abstract_dto(self):
        # Подготовка
        dto = TestReferenceDTO()

        # Действие
        result = self.convertor.convert(dto)

        # Проверка
        self.assertIsInstance(result, dict)
        self.assertIn("dto_field", result)
        self.assertEqual(result["dto_field"], "dto_value")
        self.assertIn("id", result)

    def test_convert_unconvertible_object(self):
        # Подготовка
        unconvertible_obj = "simple_string"

        # Действие
        result = self.convertor.convert(unconvertible_obj)

        # Проверка
        expected = {'value': 'simple_string', 'type': 'unconvertible'}
        self.assertEqual(result, expected)

    def test_convert_none_object(self):
        # Подготовка
        none_obj = None

        # Действие
        result = self.convertor.convert(none_obj)

        # Проверка
        expected = {'value': None, 'type': 'unconvertible'}
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()