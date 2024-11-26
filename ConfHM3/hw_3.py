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
            match = re.match(r'#\{(\+|-|\*|/|mod|sqrt) (\w+) ?(\w+)?\}', v)
            if match:
                operation, var1, var2 = match.groups()
                original_value1 = constants.get(var1, None)
                original_value2 = constants.get(var2, None) if var2 else None
                
                if original_value1 is not None:
                    if operation == '+':
                        dictionary[k] = original_value1 + (original_value2 if original_value2 is not None else 0)
                    elif operation == '-':
                        dictionary[k] = original_value1 - (original_value2 if original_value2 is not None else 0)
                    elif operation == '*':
                        dictionary[k] = original_value1 * (original_value2 if original_value2 is not None else 1)
                    elif operation == '/':
                        if original_value2 != 0:
                            dictionary[k] = original_value1 / original_value2
                    elif operation == 'mod':
                        dictionary[k] = original_value1 % (original_value2 if original_value2 is not None else 1)
                    elif operation == 'sqrt':
                        dictionary[k] = math.sqrt(original_value1)
            elif v in constants:
                dictionary[k] = constants[v]

def process_yaml(yaml_path, output_path):
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    constants = {}
    for constant in data.get('constants', []):
        match = re.match(r'var (\w+) (\d+);', constant.strip())
        if match:
            name, value = match.groups()
            constants[name] = int(value)

    dictionaries = data.get('dictionaries', [])
    for dictionary in dictionaries:
        replace_dict_values(dictionary, constants)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("[\n")
        for dictionary in dictionaries:
            for key, value in dictionary.items():
                output_file.write(f"    {key}:\n")
                for k, val in value.items():
                    output_file.write(f"        {k} => {val}\n")
        output_file.write("]\n")

# Пример использования функции
process_yaml('test.yaml', 'output.txt')