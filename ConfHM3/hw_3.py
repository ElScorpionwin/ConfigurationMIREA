import yaml
import re

def evaluate_expression(expr, constants):
    """Evaluate a constant expression in prefix form."""
    if isinstance(expr, list):
        operator = expr[0]
        if operator == '+':
            return evaluate_expression(expr[1], constants) + evaluate_expression(expr[2], constants)
        elif operator == '-':
            return evaluate_expression(expr[1], constants) - evaluate_expression(expr[2], constants)
        elif operator == '*':
            return evaluate_expression(expr[1], constants) * evaluate_expression(expr[2], constants)
        elif operator == '/':
            return evaluate_expression(expr[1], constants) / evaluate_expression(expr[2], constants)
        elif operator == 'mod':
            return evaluate_expression(expr[1], constants) % evaluate_expression(expr[2], constants)
        elif operator == 'sqrt':
            return evaluate_expression(expr[1], constants) ** 0.5
    elif isinstance(expr, str):
        if expr in constants:
            return constants[expr]
        else:
            return expr  # Вернуть строку, если она не является константой
    else:
        return expr

def replace_dict_values(dictionary, constants):
    """Замена значений в словаре константами."""
    for k, v in dictionary.items():
        if isinstance(v, dict):
            replace_dict_values(v, constants)  # Рекурсивный вызов
        elif isinstance(v, str) and v in constants:
            dictionary[k] = constants[v]

def process_yaml(yaml_path, output_path):
    with open(yaml_path, 'r', encoding='utf-8') as file:  # Убедитесь, что используем правильную кодировку
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

    expressions = data.get('expressions', [])
    results = []
    # Вычисление выражений
    for expr in expressions:
        result = evaluate_expression(expr, constants)
        results.append(result)

    # Запись результата в файл
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for name, value in constants.items():
            output_file.write(f"var {name} {value};\n")
        for dictionary in dictionaries:
            output_file.write(f"{dictionary}\n")
        for result in results:
            output_file.write(f"# {result}\n")

# Пример использования функции
process_yaml('test.yaml', 'output.txt')
