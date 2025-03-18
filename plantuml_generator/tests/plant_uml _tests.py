import unittest

from plantuml_generator.core.generator import PlantUMLGenerator


class TestPlantUMLGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = PlantUMLGenerator()

    def test_valid_uml(self):
        uml_code = """
        @startuml
        Alice -> Bob: Hello
        @enduml
        """
        result = self.generator.generate_from_code(uml_code)
        self.assertIsInstance(result, bytes)

    def test_invalid_uml(self):
        invalid_code = """
        startuml
        Alice -> Bob: Missing arrow
        @enduml
        """
        with self.assertRaises(Exception):
            self.generator.generate_from_code(invalid_code)


if __name__ == "__main__":
    unittest.main()
