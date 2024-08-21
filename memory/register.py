class Register:
    available_registers = list(range(15, 0, -1))  # regs 15, 14, 13 .. 1

    @staticmethod
    def allocate() -> int:
        register = Register.available_registers.pop()
        return register

    @staticmethod
    def free(register: int) -> None:
        Register.available_registers.append(register)
