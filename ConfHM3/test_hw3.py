import unittest
from unittest.mock import patch, mock_open
import yaml
import math

# Импортируйте функции из вашего основного файла hw2.py
from hw_3 import replace_dict_values, process_yaml

class TestYamlProcessing(unittest.TestCase):

    def test_replace_dict_values_with_constants(self):
        constants = {
            'port': 8080,
            'max_connections': 100
        }
        
        dictionary = {
            'server': {
                'host': 'localhost',
                'port': 'port',  
                'max_connections': '#{+ max_connections 10}',  
                'ssl': True
            }
        }
        
        replace_dict_values(dictionary, constants)
        
        self.assertEqual(dictionary['server']['port'], 8080)
        self.assertEqual(dictionary['server']['max_connections'], 110)

    def test_replace_dict_values_with_sqrt(self):
        constants = {
            'value': 16
        }
        
        dictionary = {
            'math_operations': {
                'sqrt_value': '#{sqrt value}',
            }
        }
        
        replace_dict_values(dictionary, constants)
        
        self.assertEqual(dictionary['math_operations']['sqrt_value'], 4.0)  # Проверяем что возвращается 4.0


    @patch('builtins.open', new_callable=mock_open)
    @patch('yaml.safe_load', return_value={
        'constants': ['var port 8080;', 'var max_connections 100;'],
        'dictionaries': [
            {
                'server': {
                    'host': 'localhost',
                    'port': 'port',  # ожидаем заменить на 8080
                    'ssl': True
                }
            }
        ]
    })
    def test_process_yaml(self, mock_yaml_load, mock_open_func):
        process_yaml('test.yaml', 'output.txt')
        
        # Проверяем, что файл output.txt открывается в режиме записи
        mock_open_func.assert_any_call('output.txt', 'w', encoding='utf-8')

        # Проверяем, что файл test.yaml открывается в режиме чтения
        # Это отдельная ассерция, а не assert_called_once_with
        mock_open_func.assert_any_call('test.yaml', 'r', encoding='utf-8')

        # Проверяем, что write вызывается с нужными аргументами
        handle = mock_open_func()
if __name__ == "__main__":
    unittest.main()