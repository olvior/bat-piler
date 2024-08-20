import memory
from variable import active_variables


def move_unknown_to_register(unknown: str, register: int) -> None:
    if is_immediate(unknown):
        memory.set_register_immediate(register, int(unknown))
    else:
        variable = active_variables[unknown]
        memory.move_address_to_register(variable.memory_address, register)


def is_immediate(string: str) -> bool:
    if string[0].isalpha():
        return False
    return True
