import file_io
from memory.register import Register

def move_address_to_register(address: int, register: int) -> None:
    found_register = Register.find_register_by_value_offset(address)

    # if none was found
    if found_register == None:
        address_register = Register.allocate()
        set_register_immediate(address_register, address)
        offset = 0
    
    # if we did find one just use it
    else:
        address_register, offset = found_register

    move_register_address_to_register(register, address_register, offset)

    if found_register == None:
        Register.free(address_register)



def move_register_to_address(value_register: int, address: int) -> None:
    found_register = Register.find_register_by_value_offset(address)
    if found_register == None:
        address_register = Register.allocate()
        set_register_immediate(address_register, address)
        offset = 0

    else:
        address_register, offset = found_register

    move_register_to_address_register(value_register, address_register, offset)

    if found_register == None:
        Register.free(address_register)



def move_register_to_address_register(value_register: int, address_register: int, offset: int = 0) -> None:
    file_io.append_to_out(f"STR r{address_register} r{value_register} {offset}")


def move_register_address_to_register(value_register: int, address_register: int, offset: int = 0) -> None:
    Register.mark_register_as_unknown(value_register)

    file_io.append_to_out(f"LOD r{address_register} r{value_register} {offset}")


def set_register_immediate(register: int, value: int) -> None:
    # we know the register's value'
    Register.set_register_value(register, value)

    text = f"LDI r{register} {value}"
    file_io.append_to_out(text)


def add_register_immediate(register: int, value: int) -> None:
    # dont know it, there is a chance we could though
    # TODO: More optimisation
    Register.mark_register_as_unknown(register)

    text = f"ADI r{register} {value}"
    file_io.append_to_out(text)
