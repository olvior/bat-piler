from typing import Callable, Dict, List

from memory import memory_utils
from memory.register import Register
from models.array import active_arrays, Array
from models.variable import active_variables
from parser_stuff.parser_utils import move_real_unknown_to_register, move_unknown_to_register


def deal_with_new(name: str, arguments: List[str]):
    if len(arguments) != 1:
        raise ValueError("Wrong number of arguments")
    if name in active_arrays:
        raise ValueError("Duplicate name")
    try:
        size = int(arguments[0])
    except ValueError:
        raise ValueError("Size must be an integer")
    Array(name, size)


def deal_with_free(name: str, arguments: List[str]):
    if len(arguments) != 0:
        raise ValueError("Wrong number of arguments")
    try:
        array = active_arrays[name]
    except KeyError as e:
        raise KeyError(f"Array {name} does not exist") from e
    array.free()


def deal_with_set(name: str, arguments: List[str]):
    array = active_arrays[name]

    index_register = Register.allocate()
    move_unknown_to_register(arguments[0], index_register)
    memory_utils.add_register_immediate(index_register, array.address)

    value_register = Register.allocate()
    move_real_unknown_to_register(arguments[1:], value_register)
    memory_utils.move_register_to_address_register(value_register, index_register)
    Register.free(index_register)
    Register.free(value_register)


def deal_with_get(name: str, arguments: List[str]):
    array = active_arrays[name]

    index_register = Register.allocate()
    move_unknown_to_register(arguments[0], index_register)
    memory_utils.add_register_immediate(index_register, array.address)

    value_register = Register.allocate()
    memory_utils.move_register_address_to_register(value_register, index_register)
    Register.free(index_register)

    variable = active_variables[arguments[1]]
    memory_utils.move_register_to_address(value_register, variable.memory_address)
    Register.free(value_register)


METHODS: Dict[str, Callable[[str, List[str]], None]] = {
    "new": deal_with_new,
    "free": deal_with_free,
    "set": deal_with_set,
    "get": deal_with_get,
}


def deal_with_array(line_segments: List[str]) -> None:
    name, method_name, *arguments = line_segments
    try:
        method = METHODS[method_name]
    except KeyError as e:
        raise KeyError(f"Array method {method_name} does not exist") from e
    method(name, arguments)
