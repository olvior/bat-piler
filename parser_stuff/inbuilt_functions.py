from typing import Callable, Dict, List

import file_io
from exceptions import InternalCompilerError
from memory import memory_utils
from memory.port import Port
from memory.register import Register
from models.variable import active_variables, Variable
from parser_stuff.array_parser import deal_with_array
from parser_stuff.parser_utils import ExpressionLoader, move_unknown_to_register, set_variable_value


def deal_with_jump(line_segments: List[str]) -> None:
    deal_with_simple("JMP", line_segments[0])


def deal_with_call(line_segments: List[str]) -> None:
    deal_with_simple("CAL", line_segments[0])


def deal_with_simple(method: str, value: str) -> None:
    file_io.append_to_out(f"{method} {value}")


def deal_with_output(line_segments: List[str]) -> None:
    if len(line_segments) < 2:
        line_segments.append("0")
    port_name = line_segments[0]
    port = Port.get_port(port_name)

    register = Register.allocate()
    move_unknown_to_register(line_segments[1], register)
    memory_utils.move_register_to_address(register, port.value)
    Register.free(register)


def deal_with_input(line_segments: List[str]) -> None:
    port_name = line_segments[0]
    port = Port.get_port(port_name)

    variable: Variable = active_variables[line_segments[1]]

    register = Register.allocate()
    memory_utils.move_address_to_register(port.value, register)
    memory_utils.move_register_to_address(register, variable.memory_address)
    Register.free(register)


def deal_with_negate(line_segments: List[str]) -> None:
    variable: Variable = active_variables[line_segments[0]]
    register = variable.reference()
    file_io.append_to_out(f"SUB r0 r{register} r{register}")
    memory_utils.move_register_to_address(register, variable.memory_address)
    variable.undo_reference()


def deal_with_set(line_segments: List[str]) -> None:
    variable_name = line_segments[0]
    variable = active_variables[variable_name]

    if line_segments[1] == "=":
        line_segments.pop(1)
    set_variable_value(line_segments[1:], variable)


def deal_with_variable_init(line_segments: List[str]) -> None:
    variable_name = line_segments[0]

    Variable(variable_name)
    variable = active_variables[variable_name]

    if line_segments[1] == "=":
        line_segments.pop(1)
    set_variable_value(line_segments[1:], variable)


def deal_with_free_variable(line_segments: List[str]) -> None:
    variable = active_variables[line_segments[0]]
    variable.free()


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
    "goto": deal_with_jump,
    "jump": deal_with_jump,
    "call": deal_with_call,
    "output": deal_with_output,
    "input": deal_with_input,
    "negate": deal_with_negate,
    "set": deal_with_set,
    "var": deal_with_variable_init,
    "free": deal_with_free_variable,
    "array": deal_with_array,
}
