from enum import Enum, auto

import file_io


class Port(Enum):
    SCREEN_SET_PIXEL_X = 240
    SCREEN_SET_PIXEL_Y = auto()
    SCREEN_DRAW_PIXEL = auto()
    SCREEN_CLEAR_PIXEL = auto()
    SCREEN_LOAD_PIXEL = auto()
    SCREEN_PUSH = auto()
    SCREEN_CLEAR = auto()
    CHAR_WRITE = auto()
    CHAR_PUSH = auto()
    CHAR_CLEAR = auto()
    NUMBER_SHOW = auto()
    NUMBER_CLEAR = auto()
    NUMBER_SET_SIGNED = auto()
    NUMBER_SET_UNSIGNED = auto()
    LOAD_RNG = auto()
    LOAD_CONTROLLER = auto()

    @staticmethod
    def get_port(name: str) -> "Port":
        try:
            return Port[name]
        except KeyError:
            print(f"Port {name} not found")
            raise KeyError


class Register:
    free_registers = list(range(15, 0, -1))  # regs 15, 14, 13 .. 1

    @staticmethod
    def allocate() -> int:
        register = Register.free_registers.pop()
        return register

    @staticmethod
    def free(register: int) -> None:
        Register.free_registers.append(register)


class Memory:
    free_addresses = list(range(239, -1, -1))  # addresses 239, 238 .. 0

    @staticmethod
    def allocate_memory() -> int:
        free_memory_address = Memory.free_addresses.pop()
        return free_memory_address

    @staticmethod
    def free(address: int) -> None:
        Memory.free_addresses.append(address)


free_registers = list(range(15, 0, -1))  # regs 15, 14, 13 .. 1
free_memory_list = list(range(239, -1, -1))  # addresses 239, 238 .. 0


def allocate_register() -> int:
    register = free_registers.pop()
    return register


def free_register(register: int) -> None:
    free_registers.append(register)


def allocate_memory() -> int:
    free_memory_address = free_memory_list.pop()
    return free_memory_address


def free_memory(address: int) -> None:
    free_memory_list.append(address)


def move_register_to_address(value_register: int, address: int) -> None:
    address_register = allocate_register()
    set_register_immediate(address_register, address)

    text = f"STR r{address_register} r{value_register}"
    free_register(address_register)
    file_io.append_to_out(text)


def move_address_to_register(address: int, register: int) -> None:
    address_register = allocate_register()
    set_register_immediate(address_register, address)

    text = f"LOD r{address_register} r{register}"

    free_register(address_register)

    file_io.append_to_out(text)


def set_register_immediate(register: int, value: int) -> None:
    text = f"LDI r{register} {value}"
    file_io.append_to_out(text)
