from typing import Optional, Dict, Tuple

class Register:
    # r15 will be reserved as io pointer
    available_registers = list(range(14, 0, -1))  # regs 14, 13, 12 .. 1

    # r0 and r15 should never change
    known_register_values: Dict[int, int] = {0: 0, 15: 248} # reg: value

    @staticmethod
    def allocate() -> int:
        # try to prioritise an unknown register, so that we accumulate as many known values as possible
        for r in Register.available_registers:
            if r in Register.known_register_values.keys():
                continue
            else:
                Register.available_registers.remove(r)
                return r

        return Register.available_registers.pop()

    @staticmethod
    def free(register: int) -> None:
        Register.available_registers.append(register)


    @staticmethod
    def find_register_by_value(value: int) -> Optional[int]:
        for r, v in Register.known_register_values.items():
            if v == value:
                return r
        
        return None

    @staticmethod
    def find_register_by_value_offset(value: int) -> Optional[Tuple[int, int]]:
        for r, v in Register.known_register_values.items():
            if value - v >= -8 and value - v <= 7:
                return (r, value - v)

        return None


    @staticmethod
    def get_register_value(register: int) -> Optional[int]:
        return Register.known_register_values.get(register)


    @staticmethod
    def set_register_value(register: int, value: int) -> None:
        Register.known_register_values[register] = value


    @staticmethod
    def mark_register_as_unknown(register: int) -> None:
        Register.known_register_values.pop(register, None)


