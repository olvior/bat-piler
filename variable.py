from typing import Optional, Dict

import memory
from memory import Memory, Register


class Variable:
    def __init__(self, name: str):
        self.register: Optional[int] = None
        self.value: Optional[int] = None
        self.name = name
        self.memory_address = Memory.allocate()
        active_variables[self.name] = self

    def set_value_immediate(self, value: int) -> None:
        self.value = value

        self.register = Register.allocate()
        memory.set_register_immediate(self.register, self.value)
        memory.move_register_to_address(self.register, self.memory_address)
        Register.free(self.register)
        self.register = None

    def reference(self) -> None:
        self.register = memory.Register.allocate()
        memory.move_address_to_register(self.memory_address, self.register)

    def undo_reference(self) -> None:
        if self.register is not None:
            Register.free(self.register)
            self.register = None

    def kill(self) -> None:
        Memory.free(self.memory_address)
        active_variables.pop(self.name)


active_variables: Dict[str, Variable] = {}
