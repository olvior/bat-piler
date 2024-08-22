import file_io
from memory.register import Register


def move_address_to_register(address: int, register: int) -> None:
    address_register = Register.allocate()
    set_register_immediate(address_register, address)
    move_register_address_to_register(register, address_register)
    Register.free(address_register)


def move_register_to_address_register(value_register: int, address_register: int) -> None:
    file_io.append_to_out(f"STR r{address_register} r{value_register}")


def move_register_to_address(value_register: int, address: int) -> None:
    address_register = Register.allocate()
    set_register_immediate(address_register, address)
    move_register_to_address_register(value_register, address_register)
    Register.free(address_register)


def move_register_address_to_register(value_register: int, address_register: int) -> None:
    file_io.append_to_out(f"LOD r{address_register} r{value_register}")


def set_register_immediate(register: int, value: int) -> None:
    text = f"LDI r{register} {value}"
    file_io.append_to_out(text)


def add_register_immediate(register: int, value: int) -> None:
    text = f"ADI r{register} {value}"
    file_io.append_to_out(text)
