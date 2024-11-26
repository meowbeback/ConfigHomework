import struct
import yaml
import sys

# Интерпретатор УВМ
class Interpreter:
    def __init__(self, binary_file, output_file, memory_range):
        self.binary_file = binary_file
        self.output_file = output_file
        self.memory_range = memory_range
        self.memory = [0] * 1024  # Простейшая память
        self.stack = []

    def execute(self):
        with open(self.binary_file, 'rb') as f:
            instructions = f.read()

        pc = 0
        while pc < len(instructions):
            opcode = instructions[pc]
            pc += 1

            if opcode == 195:  # Загрузка константы
                constant = struct.unpack('<I', instructions[pc:pc+4])[0]
                self.stack.append(constant)
                pc += 4
            elif opcode == 83:  # Чтение из памяти
                addr = self.stack.pop()
                self.stack.append(self.memory[addr])
            elif opcode == 53:  # Запись в память
                offset = struct.unpack('<H', instructions[pc:pc+2])[0]
                pc += 2
                value = self.stack.pop()
                addr = self.stack.pop() + offset
                self.memory[addr] = value
            elif opcode == 74:  # Побитовое "или"
                address = struct.unpack('<I', instructions[pc:pc+4])[0]
                pc += 4
                value1 = self.stack.pop()
                value2 = self.memory[address]
                self.stack.append(value1 | value2)

        # Сохранение памяти в диапазоне
        result = {f"memory[{i}]": self.memory[i] for i in self.memory_range}
        with open(self.output_file, 'w') as f:
            yaml.dump(result, f)

# Использование
if __name__ == "__main__":
    memory_range = range(int(sys.argv[3]), int(sys.argv[4]))
    interpreter = Interpreter(sys.argv[1], sys.argv[2], memory_range)
    interpreter.execute()
