import file_io as fio

class Ports():
    ports = {
        "SCREEN_SET_PIXEL_X": 240,
        "SCREEN_SET_PIXEL_Y": 241,
        "SCREEN_DRAW_PIXEL": 242,
        "SCREEN_CLEAR_PIXEL": 243,
        "SCREEN_LOAD_PIXEL": 244,
        "SCREEN_PUSH": 245,
        "SCREEN_CLEAR": 246,

        "CHAR_WRITE": 247,
        "CHAR_PUSH": 248,
        "CHAR_CLEAR": 249,

        "NUMBER_SHOW": 250,
        "NUMBER_CLEAR": 251,
        "NUMBER_SET_SIGNED": 252,
        "NUMBER_SET_UNSIGNED": 253,

        "LOAD_RNG": 254,
        "LOAD_CONTROLER": 255,
    }



free_registers_list = list(range(15, 0, -1)) # regs 15, 14, 13 .. 1
free_memory_list = list(range(239, -1, -1)) # addresses 239, 238 .. 0

variables_dict: dict = {}

def allocate_register():
    free_register = free_registers_list.pop()
    return free_register

def free_register(register: int):
    free_registers_list.append(register)


def allocate_memory():
    free_memory_addr = free_memory_list.pop()
    return free_memory_addr

def free_memory(addr: int):
    free_memory_list.append(addr)

def move_reg_to_addr(reg: int, addr: int):
    addr_reg = allocate_register()
    set_reg_imm(addr_reg, addr)

    text = f"STR r{addr_reg} r{reg}"
    free_register(addr_reg)
    fio.append_to_out(text)


def move_addr_to_reg(addr: int, reg: int):
    addr_reg = allocate_register()
    set_reg_imm(addr_reg, addr)

    text = f"LOD r{addr_reg} r{reg}"

    free_register(addr_reg)

    fio.append_to_out(text)

def set_reg_imm(reg: int, value):
    text = f"LDI r{reg} {value}"
    fio.append_to_out(text)

