import struct
import yaml
import sys

# Ассемблер УВМ
class Assembler:
    def __init__(self, input_file, output_file, log_file):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file

    def parse_instruction(self, line):
        """Разбор строки и преобразование в бинарный формат."""
        parts = line.strip().split()
        opcode = int(parts[0], 10)  # Код операции
        operands = list(map(int, parts[1:]))
        return opcode, operands

    def assemble(self):
        binary_data = bytearray()
        log_data = []

        with open(self.input_file, 'r') as f:
            for line in f:
                opcode, operands = self.parse_instruction(line)
                if opcode == 195:  # Загрузка константы
                    binary_data.extend(struct.pack('<BIB', opcode, operands[0], 0))
                    log_data.append({'opcode': opcode, 'constant': operands[0]})
                elif opcode == 83:  # Чтение из памяти
                    binary_data.extend(struct.pack('<BI', opcode, 0))
                    log_data.append({'opcode': opcode})
                elif opcode == 53:  # Запись в память
                    binary_data.extend(struct.pack('<BH', opcode, operands[0]))
                    log_data.append({'opcode': opcode, 'offset': operands[0]})
                elif opcode == 74:  # Побитовое "или"
                    binary_data.extend(struct.pack('<BI', opcode, operands[0]))
                    log_data.append({'opcode': opcode, 'address': operands[0]})

        # Сохранение бинарного файла
        with open(self.output_file, 'wb') as f:
            f.write(binary_data)

        # Сохранение логов в YAML
        with open(self.log_file, 'w') as f:
            yaml.dump(log_data, f)

# Использование
if __name__ == "__main__":
    assembler = Assembler(sys.argv[1], sys.argv[2], sys.argv[3])
    assembler.assemble()
