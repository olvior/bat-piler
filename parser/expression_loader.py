from typing import List

import memory
from parser.parser_utils import move_unknown_to_register


class ExpressionLoader:
    def __init__(self, expression: List[str]):
        self.expression = expression
        self.registers: List[int] = []

    def __enter__(self):
        if len(self.expression) > 3:
            self.expression = self.expression[:3]

        values = [self.expression[0], self.expression[2]]
        self.registers = [memory.allocate_register() for _ in range(len(values))]

        [move_unknown_to_register(value, register) for value, register in zip(values, self.registers)]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for register in self.registers:
            memory.free_register(register)
