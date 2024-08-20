from typing import Optional, Dict

import memory


class Variable:
    def __init__(self, name: str):
        self.register: Optional[int] = None
        self.value: Optional[int] = None
        self.name = name
        self.memory_address = memory.allocate_memory()
        active_variables[self.name] = self

    def set_value_immediate(self, value: int) -> None:
        self.value = value

        self.register = memory.allocate_register()
        memory.set_register_immediate(self.register, self.value)
        memory.move_register_to_address(self.register, self.memory_address)
        memory.free_register(self.register)
        self.register = None

    def reference(self) -> None:
        self.register = memory.allocate_register()
        memory.move_address_to_register(self.memory_address, self.register)

    def undo_reference(self) -> None:
        if self.register is not None:
            memory.free_register(self.register)
            self.register = None

    def kill(self) -> None:
        memory.free_memory(self.memory_address)
        active_variables.pop(self.name)


active_variables: Dict[str, Variable] = {}
