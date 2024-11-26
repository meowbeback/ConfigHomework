import re
import sys
def parse_array(nesting, array_str, constants):
    array_str = array_str.strip()
    if not array_str:
        return None
    if array_str[4] != "(" or array_str[-1] != ")":
        return None

    array_str = array_str[5:-1]
    result = "\n"
    for elem in array_str.split(','):
        if not elem:
            return None
        # Ожидаем, что каждый элемент может быть либо числом, либо константой, либо выражением
        result += f"{'  ' * (nesting + 1)}- {evaluate_constant(elem.strip(), constants)}\n"

    return result

def dict_check(nesting):
    if nesting > 0:
        is_dict = True
    else:
        is_dict = False
    return is_dict

def evaluate_constant(value, constants):
    if value.startswith('.') and value.endswith('.'):
        const_name = value[1:-1]
        if const_name in constants:
            return constants[const_name]
        else:
            raise ValueError(f"Constant {const_name} not found")
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Invalid constant value: {value}")

def parse_config(file_content):
    lines = file_content.splitlines()
    result = ""
    nesting = 0
    is_dict = False
    constants = {}

    for line in lines:
        line = line.strip()
        is_dict = dict_check(nesting)

        # Пустая строка
        if not line:
            continue

        # Комментарий
        elif line.startswith('//'):
            result += f"# {line[2:].strip()}\n"

        # Константы
        elif re.match(r"^var [a-zA-Z]+", line):
            const_match = re.match(r"^var [a-zA-Z]+", line)
            name = const_match.group()[4:]
            if not is_dict and line[4+len(name):7+len(name)] != " :=":
                raise ValueError(f"Wrong constant format: {line} ")

            if is_dict and line[4+len(name):4+len(name) + 3] != " ->":
                raise ValueError(f"Wrong dictionary format: {line} ")

            if is_dict:
                value = line[4 + len(name) + 4:].strip()
            else:
                value = line[4 + len(name) + 3:].strip()

            if value == "":
                raise ValueError(f"An empty constant: {line}")
            else:
                result += f"{'  ' * nesting}{name}:"

            if value == "{":
                result += "\n"
                nesting += 1
            elif value.startswith("list("):
                array = parse_array(nesting, value, constants)
                if array is None:
                    raise ValueError(f"Wrong array format: {line}")
                result += array
            else:
                # Здесь добавляется вычисление констант
                value = evaluate_constant(value, constants)
                result += f" {value}\n"
                constants[name] = value
            continue

        # Закрытие словаря
        elif line == "}":
            nesting -= 1
            continue
        else:
            raise ValueError(f"Invalid line format: {line} ")

    return result

def main():
    try:
        f = open("file1")
        text = f.read()
        yaml_text = parse_config(text)
        print(yaml_text)
    except FileNotFoundError:
        print(f"File 'test1' cannot be opened")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()