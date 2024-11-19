import yaml
import re
import math

def replace_dict_values(dictionary, constants):
    """Замена значений в словаре константами."""
    for k, v in dictionary.items():
        if isinstance(v, dict):
            replace_dict_values(v, constants)  # Рекурсивный вызов
        elif isinstance(v, str):
            # Обработка для регулярных выражений
            match = re.match(r'#\{(\+|-|\*|/|mod|sqrt) (\w+) ?(\d+)?\}', v)
            if match:
                operation, var, value = match.groups()
                if var in constants:
                    value = int(value)
                    if operation == '+':
                        dictionary[k] = constants[var] + value
                    elif operation == '-':
                        dictionary[k] = constants[var] - value
                    elif operation == '*':
                        dictionary[k] = constants[var] * value
                    elif operation == '/':
                        dictionary[k] = constants[var] / value
                    elif operation == 'mod':
                        dictionary[k] = abs(constants[var])
                    elif operation == 'sqrt':
                        dictionary[k] = math.sqrt(constants[var])
            elif v in constants:
                dictionary[k] = constants[v]  # Замена на значение из констант

def process_yaml(yaml_path, output_path):
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    constants = {}
    # Обработка констант
    for constant in data.get('constants', []):
        match = re.match(r'var (\w+) (\d+);', constant.strip())
        if match:
            name, value = match.groups()
            constants[name] = int(value)

    dictionaries = data.get('dictionaries', [])
    # Замена значений в словарях
    for dictionary in dictionaries:
        replace_dict_values(dictionary, constants)

    results = []

    # Запись результата в файл
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # Запись словарей
        output_file.write("[\n")
        for i, dictionary in enumerate(dictionaries):
            for key, value in dictionary.items():
                output_file.write(f"    {key}:\n")
                for k,val in value.items():
                    output_file.write(f"        {k} => {val}\n")
                    
        output_file.write("]\n")
        
        # Запись выражений
        for result in results:
            output_file.write(f"# {result}\n")

# Пример использования функции
process_yaml('test.yaml', 'output.txt')
