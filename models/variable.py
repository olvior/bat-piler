from typing import Dict, Optional

from memory import memory_utils, register
from memory.ram import RAM
from memory.register import Register


class Variable:
    def __init__(self, name: str, address: Optional[int] = None):
        if name in active_variables:
            raise ValueError(f'Variable {name} already defined')

        self.register: Optional[int] = None
        self.name = name
        self.memory_address = RAM.allocate() if address is None else address
        active_variables[self.name] = self

    def reference(self) -> int:
        self.register = register.Register.allocate()
        memory_utils.move_address_to_register(self.memory_address, self.register)
        return self.register

    def undo_reference(self) -> None:
        if self.register is not None:
            Register.free(self.register)
            self.register = None

    def free(self) -> None:
        RAM.free(self.memory_address)
        active_variables.pop(self.name)


active_variables: Dict[str, Variable] = {}
