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
    available_registers = list(range(15, 0, -1))  # regs 15, 14, 13 .. 1

    @staticmethod
    def allocate() -> int:
        register = Register.available_registers.pop()
        return register

    @staticmethod
    def free(register: int) -> None:
        Register.available_registers.append(register)


class Memory:
    available_addresses = list(range(239, -1, -1))  # addresses 239, 238 .. 0

    @staticmethod
    def allocate() -> int:
        memory_address = Memory.available_addresses.pop()
        return memory_address

    @staticmethod
    def free(address: int) -> None:
        Memory.available_addresses.append(address)


def move_register_to_address(value_register: int, address: int) -> None:
    address_register = Register.allocate()
    set_register_immediate(address_register, address)

    text = f"STR r{address_register} r{value_register}"
    Register.free(address_register)
    file_io.append_to_out(text)


def move_address_to_register(address: int, register: int) -> None:
    address_register = Register.allocate()
    set_register_immediate(address_register, address)

    text = f"LOD r{address_register} r{register}"

    Register.free(address_register)

    file_io.append_to_out(text)


def set_register_immediate(register: int, value: int) -> None:
    text = f"LDI r{register} {value}"
    file_io.append_to_out(text)
