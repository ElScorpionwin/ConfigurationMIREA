import unittest
import os
import yaml
from hw_3 import process_yaml


def create_test_yaml(file_path):
    """Создать тестовый yaml-файл."""
    data = {
        'constants': [
            'var a 10;',
            'var b 20;'
        ],
        'dictionaries': [
            {
                'dict1': {
                    'value1': '#{+ a 5}',
                    'value2': '#{sqrt a}',
                    'value3': '#{* a b}'
                }
            }
        ]
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)

class TestYamlProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_yaml_file = 'testing.yaml'
        cls.output_file = 'output_test.txt'
        create_test_yaml(cls.test_yaml_file)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_yaml_file)
        if os.path.exists(cls.output_file):
            os.remove(cls.output_file)

    def test_yaml_processing(self):
        process_yaml(self.test_yaml_file, self.output_file)

        # Проверяем наличие результирующего файла
        self.assertTrue(os.path.exists(self.output_file))

        # Проверяем содержимое выходного файла
        with open(self.output_file, 'r', encoding='utf-8') as f:
            output_content = f.read()

        expected_content = (
            "[\n"
            "    dict1 => [\n"
            "        value1 => 10\n"
            "        value2 => 3.1622776601683795\n"
            "        value3 => 200\n"
            "    ]\n"
            "]\n"
        )
        self.assertEqual(output_content.strip(), expected_content.strip())

if __name__ == '__main__':
    unittest.main()