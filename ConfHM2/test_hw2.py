import unittest
from unittest.mock import patch, MagicMock, mock_open
from hw2 import deps, plantuml, getting_image

class TestDependencies(unittest.TestCase):
    @patch('requests.get')
    def test_deps_no_dependencies(self, MockRequestsGet):
        # Мокаем ответ от requests.get без зависимостей
        mock_response = MagicMock()
        mock_response.text = '''
            <html>
                <body>
                    <details>
                        <summary>Not related</summary>
                    </details>
                </body>
            </html>
        '''
        MockRequestsGet.return_value = mock_response

        # Вызываем функцию deps
        result = deps("/package/test")
        
        # Проверяем, что возвращается пустой список
        self.assertEqual(result, [])

    @patch('hw2.PlantUML.processes')
    @patch('builtins.open', new_callable=mock_open)
    def test_getting_image(self, mock_open_func, MockProcesses):
        MockProcesses.return_value = b'Some binary data representing an image'

    @patch('hw2.PlantUML.processes')
    @patch('builtins.open', new_callable=mock_open)
    def test_getting_image(self, mock_open_func, MockProcesses):
        MockProcesses.return_value = b'Some binary data representing an image'
        
        # Вызов функции getting_image
        getting_image('dummy_plantuml_text', 'dummy_output_path', 'dummy_plantuml_url')

        # Проверяем, что файл открывается в режиме записи
        mock_open_func.assert_called_once_with('dummy_output_path', 'wb')
        # Проверяем, что данные записываются корректно
        mock_open_func().write.assert_called_once_with(b'Some binary data representing an image')
    def test_plantuml(self):
        deps_list = [['packageA', 'packageB'], ['packageA', 'packageC']]
        expected_output = "@startuml\n" \
                          '"packageA" --> [ ] "packageB"\n' \
                          '"packageA" --> [ ] "packageC"\n' \
                          "@enduml"
        
        result = plantuml(deps_list)
        self.assertEqual(result, expected_output)

    @patch('hw2.PlantUML.processes')
    @patch('builtins.open', new_callable=mock_open)
    def test_getting_image(self, mock_open_func, MockProcesses):
        MockProcesses.return_value = b'Some binary data representing an image'

if __name__ == "__main__":
    unittest.main()
