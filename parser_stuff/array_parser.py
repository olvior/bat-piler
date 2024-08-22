from typing import Callable, Dict, List, Tuple

from memory import memory_utils
from memory.register import Register
from models.array import active_arrays, Array
from models.variable import active_variables
from parser_stuff.parser_utils import move_real_unknown_to_register, move_unknown_to_register


def deconstruct_name_segment(name_segment: str) -> Tuple[str, str]:
    return name_segment[:name_segment.find("[")], name_segment[name_segment.find("[") + 1:name_segment.find("]")]


def calculate_index(register: int, index: str, array_address: int) -> None:
    move_unknown_to_register(index, register)
    memory_utils.add_register_immediate(register, array_address)


def deal_with_new(name_segment: str):
    name, size_segment = deconstruct_name_segment(name_segment)

    if name in active_arrays:
        raise ValueError("Duplicate name")
    try:
        size = int(size_segment)
    except ValueError:
        raise ValueError("Size must be an integer")
    Array(name, size)


def deal_with_free(name: str):
    try:
        array = active_arrays[name]
    except KeyError as e:
        raise KeyError(f"Array {name} does not exist") from e
    array.free()


def deal_with_set(name_segment: str, arguments: List[str]):
    name, index = deconstruct_name_segment(name_segment)
    array = active_arrays[name]

    index_register = Register.allocate()
    value_register = Register.allocate()
    calculate_index(index_register, index, array.address)
    move_real_unknown_to_register(arguments, value_register)
    memory_utils.move_register_to_address_register(value_register, index_register)
    Register.free(index_register)
    Register.free(value_register)


def deal_with_get(name_segment: str, arguments: List[str]):
    name, index = deconstruct_name_segment(name_segment)
    array = active_arrays[name]

    index_register = Register.allocate()
    calculate_index(index_register, index, array.address)

    value_register = Register.allocate()
    memory_utils.move_register_address_to_register(value_register, index_register)
    Register.free(index_register)

    variable = active_variables[arguments[0]]
    memory_utils.move_register_to_address(value_register, variable.memory_address)
    Register.free(value_register)


MANAGEMENT_METHODS: Dict[str, Callable[[str], None]] = {
    "new": deal_with_new,
    "free": deal_with_free,
}

VALUE_METHODS: Dict[str, Callable[[str, List[str]], None]] = {
    "=": deal_with_set,
    "->": deal_with_get,
}


def deal_with_array(line_segments: List[str]) -> None:
    try:
        method = MANAGEMENT_METHODS[line_segments[0]]
    except KeyError:
        method = VALUE_METHODS[line_segments[1]]
        method(line_segments[0], line_segments[2:])
        return
    method(line_segments[1])
