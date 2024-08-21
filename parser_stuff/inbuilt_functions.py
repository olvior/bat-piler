from typing import List, Dict, Callable

import file_io
import memory
from exceptions import InternalCompilerError
from memory import Register, Port
from parser_stuff.expression_loader import ExpressionLoader
from parser_stuff.parser_utils import move_unknown_to_register, is_immediate
from variable import active_variables, Variable


def deal_with_output(line_segments: List[str]) -> None:
    port_name = line_segments[0]
    port = Port.get_port(port_name)

    register = Register.allocate()
    move_unknown_to_register(line_segments[1], register)
    memory.move_register_to_address(register, port.value)
    Register.free(register)


def deal_with_input(line_segments: List[str]) -> None:
    port_name = line_segments[0]
    port = memory.Port.get_port(port_name)

    variable: Variable = active_variables[line_segments[1]]

    register = Register.allocate()
    memory.move_address_to_register(port.value, register)
    memory.move_register_to_address(register, variable.memory_address)
    Register.free(register)


def deal_with_negate(line_segments: List[str]) -> None:
    variable: Variable = active_variables[line_segments[0]]
    variable.reference()
    file_io.append_to_out(f"SUB r0 r{variable.register} r{variable.register}")
    memory.move_register_to_address(variable.register, variable.memory_address)
    variable.undo_reference()


def deal_with_set(line_segments: List[str]) -> None:
    variable_name = line_segments[0]
    variable = active_variables[variable_name]

    set_variable_value(line_segments[1:], variable)


def deal_with_variable_init(line_segments: List[str]) -> None:
    variable_name = line_segments[0]

    Variable(variable_name)
    variable = active_variables[variable_name]

    set_variable_value(line_segments[1:], variable)


def deal_with_free_variable(line_segments: List[str]) -> None:
    variable = active_variables[line_segments[0]]
    variable.kill()


def set_variable_value(value_expression: List[str], variable: Variable) -> None:
    if len(value_expression) == 1:
        if is_immediate(value_expression[0]):
            variable.set_value_immediate(int(value_expression[0]))
            return

        other_variable = active_variables[value_expression[0]]
        other_variable.reference()
        memory.move_register_to_address(other_variable.register, variable.memory_address)
        other_variable.undo_reference()
        return

    register = Register.allocate()

    with ExpressionLoader(value_expression) as expression_loader:
        deal_with_modifier(value_expression[1], register, *expression_loader.registers)

    memory.move_register_to_address(register, variable.memory_address)

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


def deal_with_if(line_segments: List[str], line_number: int, if_stack: List[str]) -> None:
    if_name = f".if_line_{line_number}"
    if_stack.append(if_name)

    comparison = line_segments[1]

    with ExpressionLoader(line_segments) as expression_loader:
        file_io.append_to_out(f"CMP r{expression_loader.registers[0]} r{expression_loader.registers[1]}")
        file_io.append_to_out(f"BRH {COMPARISON_KEYWORDS[comparison]} {if_name}_skip_jmp")
        file_io.append_to_out(f"JMP {if_name}")
        file_io.append_to_out(f"{if_name}_skip_jmp")


COMPARISON_KEYWORDS = {
    "==": "EQ",
    "!=": "NE",
    ">=": "GE",
    "<": "LT",
}


def deal_with_inbuilt_function(start: str, line_segments: List[str]) -> None:
    try:
        inbuilt_function = INBUILT_FUNCTIONS[start]
    except KeyError:
        raise
    try:
        inbuilt_function(line_segments)
    except Exception as e:
        raise InternalCompilerError from e


INBUILT_FUNCTIONS: Dict[str, Callable[[List[str]], None]] = {
    "output": deal_with_output,
    "input": deal_with_input,
    "negate": deal_with_negate,
    "set": deal_with_set,
    "var": deal_with_variable_init,
    "free": deal_with_free_variable,
}
