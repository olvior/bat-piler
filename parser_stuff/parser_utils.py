from typing import List, Union

import file_io
from memory import memory_utils
from memory.register import Register
from models.variable import active_variables, Variable


def move_real_unknown_to_register(unknown: Union[str, List[str]], register: int) -> None:
    if isinstance(unknown, str):
        move_unknown_to_register(unknown, register)
    elif len(unknown) == 1:
        move_unknown_to_register(unknown[0], register)
    else:
        move_expression_to_register(unknown, register)


def move_unknown_to_register(unknown: str, register: int) -> None:
    if is_immediate(unknown):
        memory_utils.set_register_immediate(register, int(unknown))
    else:
        variable = active_variables[unknown]
        memory_utils.move_address_to_register(variable.memory_address, register)


def move_expression_to_register(expression: List[str], register: int) -> None:
    with ExpressionLoader(expression) as expression_loader:
        deal_with_modifier(expression[1], register, *expression_loader.registers)

    # we remove the three we already dealt with
    for _ in range(3):
        expression.pop(0)

    while len(expression) >= 2:
        # we load the next to in
        next_modifier: str = expression.pop(0)
        right_hand_value: str = expression.pop(0)

        # allocate a register
        right_hand_register: int = Register.allocate()
        move_unknown_to_register(right_hand_value, right_hand_register)

        # add the code for the modifier
        deal_with_modifier(next_modifier, register, register, right_hand_register)
        Register.free(right_hand_register)

    print(expression)


def is_immediate(string: str) -> bool:
    if string[0].isalpha():
        return False
    return True


def set_variable_value(value_expression: List[str], variable: Variable) -> None:
    register = Register.allocate()

    move_real_unknown_to_register(value_expression, register)

    memory_utils.move_register_to_address(register, variable.memory_address)
    Register.free(register)


def deal_with_modifier(modifier: str, value_register: int, register0: int, register1: int) -> None:
    try:
        modifier_keyword = MODIFIERS[modifier]
    except KeyError:
        print(f"modifier {modifier} is not supported")
        raise KeyError
    file_io.append_to_out(f"{modifier_keyword} r{register0} r{register1} r{value_register}")


MODIFIERS = {
    "+": "ADD",
    '-': "SUB",
    'NOR': "NOR",
    'AND': "AND",
    '&&': "AND",
    'XOR': "XOR",
    '^': "XOR",
}


class ExpressionLoader:
    def __init__(self, expression: List[str]):
        self.expression = expression
        self.registers: List[int] = []

    def __enter__(self):
        if len(self.expression) > 3:
            self.expression = self.expression[:3]

        values = [self.expression[0], self.expression[2]]
        self.registers = [Register.allocate() for _ in range(len(values))]

        [move_unknown_to_register(value, register) for value, register in zip(values, self.registers)]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for register in self.registers:
            Register.free(register)
